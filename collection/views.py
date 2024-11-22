from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Collection, CollectionMovie
from .serializers import CollectionSerializer, CollectionListSerializer
from collections import Counter
from rest_framework.exceptions import NotFound


class CollectionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get user's collections
        collections = Collection.objects.filter(user=request.user)
        collection_data = CollectionListSerializer(collections, many=True).data

        # Calculate favorite genres
        all_movies = CollectionMovie.objects.filter(collection__user=request.user)
        genres_list = []
        for movie in all_movies:
            genres_list.extend([g.strip() for g in movie.genres.split(',')])

        # Get top 3 genres
        genre_counter = Counter(genres_list)
        top_genres = [genre for genre, _ in genre_counter.most_common(3)]
        favourite_genres = ", ".join(top_genres) if top_genres else ""

        return Response({
            "is_success": True,
            "data": {
                "collections": collection_data,
                "favourite_genres": favourite_genres
            }
        })

    def post(self, request):
        serializer = CollectionSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            collection = serializer.save()
            return Response({
                'collection_uuid': collection.uuid
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CollectionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_collection(self, uuid, user):
        try:
            return Collection.objects.get(uuid=uuid, user=user)
        except Collection.DoesNotExist:
            raise NotFound("Collection not found.")

    def get(self, request, collection_uuid):
        collection = self.get_collection(collection_uuid, request.user)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)

    def put(self, request, collection_uuid):
        collection = self.get_collection(collection_uuid, request.user)
        serializer = CollectionSerializer(
            collection,
            data=request.data,
            context={'request': request},
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, collection_uuid):
        collection = self.get_collection(collection_uuid, request.user)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)