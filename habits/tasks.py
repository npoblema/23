from celery import shared_task
import requests
from django.conf import settings
from habits.models import Habit

@shared_task
def send_telegram_reminder(habit_id):
    try:
        habit = Habit.objects.get(id=habit_id)
        user = habit.user
        if not user.telegram_id:
            print(f"У пользователя {user.username} не указан telegram_id")
            return

        message = f"Напоминание: {habit.action} в {habit.time} в {habit.place}"
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        params = {
            "chat_id": user.telegram_id,
            "text": message,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        print(f"Уведомление отправлено: {message}")
    except Exception as e:
        print(f"Ошибка отправки уведомления: {e}")