from django.urls import path
from .views import CollectionListCreateView, CollectionDetailView

urlpatterns = [
    path('collection/', CollectionListCreateView.as_view(), name='collection-list-create'),
    path('collection/<uuid:collection_uuid>/', CollectionDetailView.as_view(), name='collection-detail'),
]