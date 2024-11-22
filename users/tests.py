import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestUserRegistration:
    def setup_method(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }

    def test_user_registration_success(self):
        response = self.client.post(self.register_url, self.user_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'access_token' in response.data
        assert User.objects.filter(username='testuser').exists()

    def test_user_registration_duplicate_username(self):
        User.objects.create_user(username='testuser', password='password123')
        response = self.client.post(self.register_url, self.user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST