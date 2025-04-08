from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from habits.models import Habit
from habits.serializers import HabitSerializer
from habits.tasks import send_telegram_reminder
from users.models import CustomUser
from unittest.mock import patch
from datetime import time
import json

class HabitTests(TestCase):
    def setUp(self):
        # Очищаем базу данных перед каждым тестом
        Habit.objects.all().delete()
        CustomUser.objects.all().delete()

        # Создаём тестового пользователя
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            telegram_id='5106855055'
        )
        self.client = APIClient()
        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user)

        # Создаём тестовую привычку
        self.habit = Habit.objects.create(
            user=self.user,
            place="дома",
            time=time(18, 42),
            action="сделать зарядку",
            is_pleasant=False,
            periodicity=1,
            duration=60,
            is_public=True
        )

    def test_create_habit(self):
        """Тест создания привычки"""
        url = reverse('habit-create')
        data = {
            "place": "дома",
            "time": "18:45:00",
            "action": "сделать зарядку 2",
            "is_pleasant": False,
            "periodicity": 1,
            "duration": 60,
            "is_public": True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)  # Одна привычка из setUp, вторая — новая
        self.assertEqual(Habit.objects.last().action, "сделать зарядку 2")

    def test_list_habits(self):
        """Тест получения списка привычек пользователя"""
        url = reverse('habit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Учитываем пагинацию: данные в response.data['results']
        self.assertEqual(len(response.data['results']), 1)  # Одна привычка у пользователя
        self.assertEqual(response.data['results'][0]['action'], "сделать зарядку")

    def test_list_public_habits(self):
        """Тест получения списка публичных привычек"""
        url = reverse('public-habit-list')
        # Создаём ещё одну публичную привычку от другого пользователя
        other_user = CustomUser.objects.create_user(
            username='otheruser',
            email='otheruser@example.com',
            password='testpassword'
        )
        Habit.objects.create(
            user=other_user,
            place="парк",
            time=time(19, 00),
            action="пробежка",
            is_pleasant=False,
            periodicity=1,
            duration=120,
            is_public=True
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Учитываем пагинацию: данные в response.data['results']
        self.assertEqual(len(response.data['results']), 2)  # Две публичные привычки

    def test_habit_serializer(self):
        """Тест сериализатора HabitSerializer"""
        serializer = HabitSerializer(instance=self.habit)
        data = serializer.data
        self.assertEqual(data['place'], "дома")
        self.assertEqual(data['action'], "сделать зарядку")
        self.assertEqual(data['is_public'], True)

    def test_habit_model_str(self):
        """Тест метода __str__ модели Habit"""
        self.assertEqual(str(self.habit), "сделать зарядку в 18:42:00 в дома")

    @patch('habits.tasks.requests.get')
    def test_send_telegram_reminder_success(self, mock_get):
        """Тест успешной отправки Telegram-уведомления"""
        # Мокируем успешный ответ от Telegram API
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"ok": True}

        # Вызываем задачу
        result = send_telegram_reminder(self.habit.id)

        # Проверяем, что запрос был отправлен
        self.assertTrue(mock_get.called)
        call_args = mock_get.call_args[1]['params']
        self.assertEqual(call_args['chat_id'], '5106855055')
        self.assertEqual(call_args['text'], "Напоминание: сделать зарядку в 18:42:00 в дома")

    @patch('habits.tasks.requests.get')
    def test_send_telegram_reminder_no_telegram_id(self, mock_get):
        """Тест отправки Telegram-уведомления, если telegram_id отсутствует"""
        # Удаляем telegram_id у пользователя
        self.user.telegram_id = None
        self.user.save()

        # Вызываем задачу
        result = send_telegram_reminder(self.habit.id)

        # Проверяем, что запрос не был отправлен
        self.assertFalse(mock_get.called)

    @patch('habits.tasks.requests.get')
    def test_send_telegram_reminder_failure(self, mock_get):
        """Тест ошибки при отправке Telegram-уведомления"""
        # Мокируем ошибку от Telegram API
        mock_get.return_value.status_code = 400
        mock_get.return_value.raise_for_status.side_effect = Exception("Telegram API error")

        # Вызываем задачу
        result = send_telegram_reminder(self.habit.id)

        # Проверяем, что запрос был отправлен
        self.assertTrue(mock_get.called)