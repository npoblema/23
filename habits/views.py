from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from .models import Habit
from .serializers import HabitSerializer


# Настройка пагинации: 5 привычек на страницу
class HabitPagination(PageNumberPagination):
    page_size = 5


# Право доступа: только владелец может изменять свои привычки
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешаем чтение всем (GET-запросы)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешаем запись только владельцу привычки
        return obj.user == request.user


# Список привычек пользователя и создание новой
class HabitListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [permissions.IsAuthenticated]  # Только авторизованные пользователи

    def get_queryset(self):
        # Возвращаем только привычки текущего пользователя
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # При создании привязываем привычку к текущему пользователю
        serializer.save(user=self.request.user)


# Список публичных привычек
class PublicHabitListView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)
    pagination_class = HabitPagination
    permission_classes = [permissions.AllowAny]  # Доступно всем, даже неавторизованным


# Просмотр, редактирование и удаление привычки
class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]  # Только владелец может изменять