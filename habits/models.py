from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    periodicity = models.PositiveIntegerField(default=1)  # Периодичность в днях
    reward = models.CharField(max_length=255, null=True, blank=True)
    duration = models.PositiveIntegerField()  # Длительность в секундах
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.action} в {self.time} в {self.place}"