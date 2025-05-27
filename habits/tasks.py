import logging

import requests
from celery import shared_task
from django.conf import settings

from habits.models import Habit

logger = logging.getLogger(__name__)

@shared_task
def send_telegram_reminder(habit_id):
    try:
        habit = Habit.objects.get(id=habit_id)
        user = habit.user
        if not user.telegram_id:
            logger.warning(f"User {user.email} has no telegram_id")
            return False

        message = f"Напоминание: {habit.action} в {habit.time} в {habit.place}"
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        params = {
            'chat_id': user.telegram_id,
            'text': message
        }
        response = requests.post(url, params=params)
        if response.status_code == 200:
            logger.info(f"Successfully sent reminder to {user.telegram_id} for habit {habit.id}")
            return True
        else:
            logger.error(f"Failed to send reminder: {response.status_code} {response.text}")
            return False
    except Habit.DoesNotExist:
        logger.error(f"Habit with id {habit_id} does not exist")
        return False
    except Exception as e:
        logger.error(f"Error sending reminder: {str(e)}")
        return False