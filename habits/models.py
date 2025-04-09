from django.db import models
from users.models import CustomUser

class Habit(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=100)
    time = models.TimeField()
    action = models.CharField(max_length=100)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    periodicity = models.PositiveIntegerField(default=1)
    reward = models.CharField(max_length=100, blank=True, null=True)
    duration = models.PositiveIntegerField()
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.action} в {self.place} в {self.time}"