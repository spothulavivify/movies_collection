import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .middleware import RequestCountMiddleware

User = get_user_model()


@pytest.mark.django_db
class TestRequestCounter:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        RequestCountMiddleware.reset_request_count()

    def test_get_request_count(self):
        url = reverse('request-count')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'requests' in response.data
        assert isinstance(response.data['requests'], int)

    def test_reset_request_count(self):
        self.client.get(reverse('request-count'))
        self.client.get(reverse('request-count'))

        # Reset counter
        url = reverse('request-count-reset')
        response = self.client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'request count reset successfully'

        # Verifying counter was reset
        count_response = self.client.get(reverse('request-count'))
        assert count_response.data['requests'] == 1  # This request itself counts