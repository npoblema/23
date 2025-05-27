# habits/urls.py
from django.urls import path

from .views import (HabitCreateAPIView, HabitDestroyAPIView, HabitListAPIView,
                    HabitUpdateAPIView, PublicHabitListAPIView)

urlpatterns = [
    path('habits/', HabitListAPIView.as_view(), name='habit-list'),
    path('habits/public/', PublicHabitListAPIView.as_view(), name='public-habit-list'),
    path('habits/create/', HabitCreateAPIView.as_view(), name='habit-create'),
    path('habits/<int:pk>/update/', HabitUpdateAPIView.as_view(), name='habit-update'),
    path('habits/<int:pk>/delete/', HabitDestroyAPIView.as_view(), name='habit-delete'),
]