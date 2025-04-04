from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    telegram_id = models.CharField(max_length=50, blank=True, null=True, help_text="Telegram ID для уведомлений")

    def __str__(self):
        return self.username