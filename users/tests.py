import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_register_user(api_client):
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }
    response = api_client.post('/api/users/register/', data, format='json')
    assert response.status_code == 201
    assert "access" in response.data  # Обновлено: ожидаем 'access', а не 'token'
    assert "refresh" in response.data
    assert "user" in response.data
    assert response.data['user']['username'] == "testuser"

@pytest.mark.django_db
def test_login_user(api_client):
    user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
    data = {
        "username": "testuser",
        "password": "testpass123"
    }
    response = api_client.post('/api/users/login/', data, format='json')
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data
    assert "user" in response.data
    assert response.data['user']['username'] == "testuser"

@pytest.mark.django_db
def test_login_invalid_credentials(api_client):
    data = {
        "username": "wronguser",
        "password": "wrongpass"
    }
    response = api_client.post('/api/users/login/', data, format='json')
    assert response.status_code == 401
    assert "detail" in response.data  # Обновлено: ожидаем 'detail', а не 'error'
    assert response.data['detail'] == "No active account found with the given credentials"

@pytest.mark.django_db
def test_refresh_token(api_client):
    user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    login_response = api_client.post('/api/users/login/', login_data, format='json')
    refresh_token = login_response.data['refresh']
    data = {
        "refresh": refresh_token
    }
    response = api_client.post('/api/users/token/refresh/', data, format='json')
    assert response.status_code == 200
    assert "access" in response.data