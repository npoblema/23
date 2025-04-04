import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from habits.models import Habit
from habits.serializers import HabitSerializer

User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', email='test@example.com', password='testpass')

@pytest.fixture
def habit(user):
    return Habit.objects.create(
        user=user,
        place="дома",
        time="08:00:00",
        action="сделать зарядку",
        is_pleasant=False,
        periodicity=1,
        duration=60,
        is_public=True
    )

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_habit_model_validation_duration():
    user = User.objects.create_user(username='testuser2', email='test2@example.com', password='testpass')
    habit = Habit(
        user=user,
        place="дома",
        time="08:00:00",
        action="сделать зарядку",
        is_pleasant=False,
        periodicity=1,
        duration=121,  # больше 120 секунд
        is_public=True
    )
    with pytest.raises(Exception) as excinfo:
        habit.full_clean()
    assert "Duration must be less than or equal to 120 seconds" in str(excinfo.value)

@pytest.mark.django_db
def test_habit_model_validation_reward_and_related_habit():
    user = User.objects.create_user(username='testuser3', email='test3@example.com', password='testpass')
    habit = Habit(
        user=user,
        place="дома",
        time="08:00:00",
        action="сделать зарядку",
        is_pleasant=False,
        periodicity=1,
        duration=60,
        is_public=True,
        reward="награда",
        related_habit=Habit.objects.create(
            user=user,
            place="дома",
            time="09:00:00",
            action="полезная привычка",
            is_pleasant=True,
            periodicity=1,
            duration=60,
            is_public=True
        )
    )
    with pytest.raises(Exception) as excinfo:
        habit.full_clean()
    assert "Habit cannot have both a reward and a related habit" in str(excinfo.value)

@pytest.mark.django_db
def test_habit_serializer_valid_data(user):
    data = {
        "place": "дома",
        "time": "08:00:00",
        "action": "сделать зарядку",
        "is_pleasant": False,
        "periodicity": 1,
        "duration": 60,
        "is_public": True
    }
    serializer = HabitSerializer(data=data)
    assert serializer.is_valid()
    habit = serializer.save(user=user)
    assert habit.place == "дома"
    assert habit.action == "сделать зарядку"

@pytest.mark.django_db
def test_habit_serializer_invalid_duration():
    data = {
        "place": "дома",
        "time": "08:00:00",
        "action": "сделать зарядку",
        "is_pleasant": False,
        "periodicity": 1,
        "duration": 121,  # больше 120 секунд
        "is_public": True
    }
    serializer = HabitSerializer(data=data)
    assert not serializer.is_valid()
    assert "duration" in serializer.errors

@pytest.mark.django_db
def test_create_habit(api_client, user):
    api_client.force_authenticate(user=user)
    data = {
        "place": "дома",
        "time": "08:00:00",
        "action": "сделать зарядку",
        "is_pleasant": False,
        "periodicity": 1,
        "duration": 60,
        "is_public": True
    }
    response = api_client.post(reverse('habits:habit-list'), data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['place'] == "дома"
    assert response.data['action'] == "сделать зарядку"

@pytest.mark.django_db
def test_list_public_habits(api_client, habit):
    response = api_client.get(reverse('habits:public-habits'))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['place'] == "дома"

@pytest.mark.django_db
def test_update_habit_permission(api_client, user, habit):
    another_user = User.objects.create_user(username='anotheruser', email='another@example.com', password='testpass')
    api_client.force_authenticate(user=another_user)
    response = api_client.patch(reverse('habits:habit-detail', args=[habit.id]), {'place': 'офис'}, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_list_habits_authenticated(api_client, user, habit):
    api_client.force_authenticate(user=user)
    response = api_client.get(reverse('habits:habit-list'))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['place'] == "дома"


@pytest.mark.django_db
def test_habit_model_validation_periodicity():
    user = User.objects.create_user(username='testuser4', email='test4@example.com', password='testpass')
    habit = Habit(
        user=user,
        place="дома",
        time="08:00:00",
        action="сделать зарядку",
        is_pleasant=False,
        periodicity=0,  # меньше 1
        duration=60,
        is_public=True
    )
    with pytest.raises(Exception) as excinfo:
        habit.full_clean()
    assert "Periodicity must be at least 1 day" in str(excinfo.value)


@pytest.mark.django_db
def test_habit_serializer_invalid_related_habit(user):
    related_habit = Habit.objects.create(
        user=user,
        place="дома",
        time="09:00:00",
        action="неприятная привычка",
        is_pleasant=False,  # должна быть приятной
        periodicity=1,
        duration=60,
        is_public=True
    )
    data = {
        "place": "дома",
        "time": "08:00:00",
        "action": "сделать зарядку",
        "is_pleasant": False,
        "periodicity": 1,
        "duration": 60,
        "is_public": True,
        "related_habit": related_habit.id
    }
    serializer = HabitSerializer(data=data)
    assert not serializer.is_valid()
    assert "related_habit" in serializer.errors

@pytest.mark.django_db
def test_delete_habit(api_client, user, habit):
    api_client.force_authenticate(user=user)
    response = api_client.delete(reverse('habits:habit-detail', args=[habit.id]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Habit.objects.count() == 0