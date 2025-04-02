import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

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
    assert "token" in response.data
    assert User.objects.count() == 1
    assert Token.objects.count() == 1

@pytest.mark.django_db
def test_login_user(api_client):
    user = User.objects.create_user(username="testuser", password="testpass123")
    data = {
        "username": "testuser",
        "password": "testpass123"
    }
    response = api_client.post('/api/users/login/', data, format='json')
    assert response.status_code == 200
    assert "token" in response.data

@pytest.mark.django_db
def test_login_invalid_credentials(api_client):
    data = {
        "username": "wronguser",
        "password": "wrongpass"
    }
    response = api_client.post('/api/users/login/', data, format='json')
    assert response.status_code == 401
    assert "error" in response.data