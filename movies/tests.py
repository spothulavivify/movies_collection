import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from .services import MovieService
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestMovieAPI:
    def setup_method(self):
        self.client = APIClient()
        self.movies_url = reverse('movie-list')

        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Authenticate the client
        self.client.force_authenticate(user=self.user)

    @patch.object(MovieService, 'get_movies')
    def test_movie_list_success(self, mock_get_movies):
        mock_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'data': [
                {
                    'title': 'Test Movie 1',
                    'description': 'Description 1',
                    'genres': 'Action,Drama',
                    'uuid': '123e4567-e89b-12d3-a456-426614174000'
                },
                {
                    'title': 'Test Movie 2',
                    'description': 'Description 2',
                    'genres': 'Comedy',
                    'uuid': '123e4567-e89b-12d3-a456-426614174001'
                }
            ]
        }
        mock_get_movies.return_value = mock_data

        response = self.client.get(self.movies_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == mock_data