import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Habit
from .serializers import HabitSerializer
from datetime import time
from habits.tasks import send_telegram_reminder

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def habit(user, mocker):
    mocker.patch('habits.tasks.send_telegram_reminder.apply_async')  # Мокаем задачу
    return Habit.objects.create(
        user=user,
        place="дома",
        time=time(8, 0),
        action="сделать зарядку",
        is_pleasant=False,
        periodicity=1,
        duration=60,
        is_public=True
    )

# Тесты модели
@pytest.mark.django_db
def test_habit_model_validation_duration(user):
    habit = Habit(user=user, place="дома", time=time(8, 0), action="тест", duration=150)
    with pytest.raises(Exception) as excinfo:
        habit.full_clean()
    assert "Время выполнения не должно превышать 120 секунд" in str(excinfo.value)

@pytest.mark.django_db
def test_habit_model_validation_reward_and_related_habit(user):
    pleasant_habit = Habit.objects.create(user=user, place="парк", time=time(9, 0), action="гулять", is_pleasant=True)
    habit = Habit(user=user, place="дома", time=time(8, 0), action="тест", reward="конфета", related_habit=pleasant_habit)
    with pytest.raises(Exception) as excinfo:
        habit.full_clean()
    assert "Нельзя указать одновременно вознаграждение и связанную привычку" in str(excinfo.value)

# Тесты сериализатора
@pytest.mark.django_db
def test_habit_serializer_valid_data(user):
    data = {
        "place": "дома",
        "time": "08:00",
        "action": "сделать зарядку",
        "is_pleasant": False,
        "periodicity": 1,
        "duration": 60,
        "is_public": True
    }
    serializer = HabitSerializer(data=data, context={'request': type('Request', (), {'user': user})()})
    assert serializer.is_valid(), serializer.errors

@pytest.mark.django_db
def test_habit_serializer_invalid_duration(user):
    data = {
        "place": "дома",
        "time": "08:00",
        "action": "тест",
        "duration": 150
    }
    serializer = HabitSerializer(data=data, context={'request': type('Request', (), {'user': user})()})
    assert not serializer.is_valid()
    assert "Время выполнения не должно превышать 120 секунд" in str(serializer.errors["non_field_errors"][0])

# Тесты API
@pytest.mark.django_db
def test_create_habit(api_client, user):
    api_client.force_authenticate(user=user)
    data = {
        "place": "дома",
        "time": "08:00",
        "action": "сделать зарядку",
        "is_pleasant": False,
        "periodicity": 1,
        "duration": 60,
        "is_public": True
    }
    response = api_client.post('/api/habits/', data, format='json')
    if response.status_code != 201:
        print(response.data)  # Выводим ошибки валидации
    assert response.status_code == 201
    assert Habit.objects.count() == 1

@pytest.mark.django_db
def test_list_public_habits(api_client, habit):
    response = api_client.get('/api/habits/public/')
    assert response.status_code == 200
    assert len(response.data['results']) == 1

@pytest.mark.django_db
def test_update_habit_permission(api_client, user, habit):
    another_user = User.objects.create_user(username='otheruser', password='otherpass')
    api_client.force_authenticate(user=another_user)
    data = {"action": "обновлённое действие"}
    response = api_client.patch(f'/api/habits/{habit.id}/', data, format='json')
    assert response.status_code == 403  # Доступ запрещён для другого пользователя

@pytest.mark.django_db
def test_list_habits_authenticated(api_client, user, habit):
    api_client.force_authenticate(user=user)
    response = api_client.get('/api/habits/')
    assert response.status_code == 200
    assert len(response.data['results']) == 1