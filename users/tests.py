from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'username': 'testuser',
            'telegram_id': '5106855055'
        }

    def test_register_user(self):
        """Тест регистрации пользователя"""
        url = reverse('register')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertNotIn('refresh', response.data)  # Токены не должны возвращаться
        self.assertNotIn('access', response.data)
        self.assertEqual(response.data['user']['email'], self.user_data['email'])
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_login_user(self):
        """Тест авторизации пользователя"""
        # Сначала регистрируем пользователя
        CustomUser.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            username='testuser'
        )
        url = reverse('token_obtain_pair')
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertEqual(response.data['user']['email'], 'testuser@example.com')

    def test_login_invalid_credentials(self):
        """Тест авторизации с неверными данными"""
        url = reverse('token_obtain_pair')
        data = {
            'email': 'wronguser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token(self):
        """Тест обновления токена"""
        # Регистрируем пользователя и получаем токены
        CustomUser.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            username='testuser'
        )
        login_url = reverse('token_obtain_pair')
        login_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        refresh_token = login_response.data['refresh']

        # Обновляем токен
        url = reverse('token_refresh')
        data = {'refresh': refresh_token}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)