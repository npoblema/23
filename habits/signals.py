from django.db.models.signals import post_save
from django.dispatch import receiver
from habits.models import Habit
from habits.tasks import send_telegram_reminder
from datetime import datetime

@receiver(post_save, sender=Habit)
def schedule_habit_reminder(sender, instance, created, **kwargs):
    if created:
        now = datetime.now().time()
        habit_time = instance.time
        delay = (datetime.combine(datetime.today(), habit_time) - datetime.combine(datetime.today(), now)).total_seconds()
        print(f"Текущее время: {now}, Время привычки: {habit_time}, Задержка: {delay} секунд")
        if delay > 0:
            send_telegram_reminder.apply_async((instance.id,), countdown=delay)
        else:
            print("Время привычки уже прошло, уведомление не запланировано")