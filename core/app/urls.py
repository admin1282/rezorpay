from .views import TikitCreateAPIView
from django.urls import path

urlpatterns = [
    path('tikit/', TikitCreateAPIView.as_view())
]