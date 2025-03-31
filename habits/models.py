from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .tasks import send_telegram_reminder
from datetime import datetime, timedelta


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits")
    place = models.CharField(max_length=100, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=200, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'is_pleasant': True},
        verbose_name="Связанная привычка"
    )
    periodicity = models.PositiveIntegerField(default=1, verbose_name="Периодичность (дни)")
    reward = models.CharField(max_length=200, null=True, blank=True, verbose_name="Вознаграждение")
    duration = models.PositiveIntegerField(default=60, verbose_name="Время выполнения (секунды)")
    is_public = models.BooleanField(default=False, verbose_name="Публичная привычка")

    def clean(self):
        if self.reward and self.related_habit:
            raise ValidationError("Нельзя указать одновременно вознаграждение и связанную привычку.")
        if self.duration > 120:
            raise ValidationError("Время выполнения не должно превышать 120 секунд.")
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError("Приятная привычка не может иметь вознаграждение или связанную привычку.")
        if self.periodicity < 1 or self.periodicity > 7:
            raise ValidationError("Периодичность должна быть от 1 до 7 дней.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        # Планируем напоминание после сохранения
        self.schedule_reminder(chat_id='123456789')  # Замени на свой chat_id

    def schedule_reminder(self, chat_id):
        message = f"Напоминание: {self.action} в {self.time} в {self.place}"
        eta = datetime.combine(datetime.today(), self.time)
        if eta < datetime.now():
            eta += timedelta(days=1)  # Если время прошло, переносим на завтра
        send_telegram_reminder.apply_async((chat_id, message), eta=eta)

    def __str__(self):
        return f"{self.action} в {self.time} в {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"