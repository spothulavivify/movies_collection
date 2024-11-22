from django.db import models
from django.conf import settings
import uuid

class Collection(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

class CollectionMovie(models.Model):
    collection = models.ForeignKey(Collection, related_name='movies', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    genres = models.CharField(max_length=255)
    uuid = models.UUIDField(default=uuid.uuid4)
