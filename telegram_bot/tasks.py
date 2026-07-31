from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from telegram_bot.services import send_telegram_message


@shared_task
def send_telegram_message_task(chat_id, message):
    send_telegram_message(
        chat_id,
        message,
    )


@shared_task
def send_habit_reminders():
    now = timezone.localtime()

    current_time = now.time().replace(
        second=0,
        microsecond=0,
    )

    habits = Habit.objects.filter(
        time=current_time,
    )

    for habit in habits:
        user = habit.user

        if user.telegram_chat_id:
            send_telegram_message_task.delay(
                user.telegram_chat_id,
                f"Напоминание: {habit.action}",

            )
