# habit_tracker/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('habits.urls')),  # Эта строка вызывает ошибку
    path('api/users/', include('users.urls')),  # Если у тебя есть приложение users
]