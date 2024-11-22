from rest_framework import serializers
from .models import Collection, CollectionMovie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionMovie
        fields = ['title', 'description', 'genres', 'uuid']


class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)

    class Meta:
        model = Collection
        fields = ['uuid', 'title', 'description', 'movies']
        read_only_fields = ['uuid']

    def create(self, validated_data):
        movies_data = validated_data.pop('movies')
        collection = Collection.objects.create(
            user=self.context['request'].user,
            **validated_data
        )

        for movie_data in movies_data:
            CollectionMovie.objects.create(collection=collection, **movie_data)
        return collection

    def update(self, instance, validated_data):
        movies_data = validated_data.pop('movies', None)

        # Update collection fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update movies if provided
        if movies_data is not None:
            instance.movies.all().delete()  # Remove existing movies
            for movie_data in movies_data:
                CollectionMovie.objects.create(collection=instance, **movie_data)

        return instance


class CollectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['title', 'uuid', 'description']