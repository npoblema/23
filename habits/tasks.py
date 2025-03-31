from celery import shared_task
from telegram import Bot
import os
from dotenv import load_dotenv
load_dotenv()


@shared_task
def send_telegram_reminder(chat_id, message):
    bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
    bot.send_message(chat_id=chat_id, text=message)
