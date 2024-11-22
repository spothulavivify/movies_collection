from django.urls import path
from .views import RequestCountView, RequestCountResetView

urlpatterns = [
    path('request-count/', RequestCountView.as_view(), name='request-count'),
    path('request-count/reset/', RequestCountResetView.as_view(), name='request-count-reset'),
]