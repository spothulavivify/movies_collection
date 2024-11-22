import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Collection, CollectionMovie
import uuid

User = get_user_model()


@pytest.mark.django_db
class TestCollections:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        # Test data
        self.collection_data = {
            'title': 'My Collection',
            'description': 'Test Collection',
            'movies': [
                {
                    'title': 'Movie 1',
                    'description': 'Description 1',
                    'genres': 'Action,Drama',
                    'uuid': str(uuid.uuid4())
                }
            ]
        }

    def test_create_collection(self):
        url = reverse('collection-list-create')
        response = self.client.post(url, self.collection_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'collection_uuid' in response.data

        # Verify collection was created
        collection_uuid = response.data['collection_uuid']
        collection = Collection.objects.get(uuid=collection_uuid)
        assert collection.title == self.collection_data['title']
        assert collection.movies.count() == 1

    def test_list_collections(self):
        # Create a collection first
        collection = Collection.objects.create(
            user=self.user,
            title='Test Collection',
            description='Description'
        )
        CollectionMovie.objects.create(
            collection=collection,
            title='Test Movie',
            description='Description',
            genres='Action',
            uuid=uuid.uuid4()
        )

        url = reverse('collection-list-create')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_success'] is True
        assert len(response.data['data']['collections']) == 1
        assert 'favourite_genres' in response.data['data']