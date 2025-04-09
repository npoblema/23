from django.test import TestCase
from rest_framework.test import APIClient
from habits.models import Habit
from users.models import CustomUser
from datetime import time
from unittest.mock import patch
from django.conf import settings

class HabitTests(TestCase):
    def setUp(self):
        # Очищаем базу данных перед каждым тестом
        Habit.objects.all().delete()
        CustomUser.objects.all().delete()

        # Создаём тестового пользователя
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            username='testuser',
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



    def test_list_habits(self):
        """Тест получения списка привычек пользователя"""
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

    def test_list_public_habits(self):
        """Тест получения списка публичных привычек"""
        response = self.client.get('/api/habits/public/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

    def test_habit_model_str(self):
        """Тест метода __str__ модели Habit"""
        self.assertEqual(str(self.habit), "сделать зарядку в дома в 18:42:00")

    def test_habit_serializer(self):
        """Тест сериализатора Habit"""
        from habits.serializers import HabitSerializer
        serializer = HabitSerializer(instance=self.habit)
        data = serializer.data
        self.assertEqual(data['action'], 'сделать зарядку')
        self.assertEqual(data['place'], 'дома')

    @patch('habits.tasks.requests.post')
    def test_send_telegram_reminder_success(self, mock_post):
        """Тест успешной отправки напоминания в Telegram"""
        mock_post.return_value.status_code = 200
        from habits.tasks import send_telegram_reminder
        result = send_telegram_reminder(self.habit.id)
        self.assertTrue(result)
        mock_post.assert_called_once_with(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            params={
                'chat_id': self.user.telegram_id,
                'text': f"Напоминание: {self.habit.action} в {self.habit.time} в {self.habit.place}"
            }
        )

    @patch('habits.tasks.requests.post')
    def test_send_telegram_reminder_failure(self, mock_post):
        """Тест неудачной отправки напоминания в Telegram"""
        mock_post.return_value.status_code = 400
        mock_post.return_value.text = "Bad Request"
        from habits.tasks import send_telegram_reminder
        result = send_telegram_reminder(self.habit.id)
        self.assertFalse(result)
        mock_post.assert_called_once_with(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            params={
                'chat_id': self.user.telegram_id,
                'text': f"Напоминание: {self.habit.action} в {self.habit.time} в {self.habit.place}"
            }
        )

    def test_send_telegram_reminder_no_telegram_id(self):
        """Тест отправки напоминания без telegram_id"""
        user_no_telegram = CustomUser.objects.create_user(
            email='notguser@example.com',
            password='testpassword',
            username='notguser'
        )
        habit = Habit.objects.create(
            user=user_no_telegram,
            place="дома",
            time=time(18, 42),
            action="сделать зарядку",
            is_pleasant=False,
            periodicity=1,
            duration=60,
            is_public=True
        )
        from habits.tasks import send_telegram_reminder
        result = send_telegram_reminder(habit.id)
        self.assertFalse(result)