from unittest.mock import patch, Mock
import requests
import pytest

from django.contrib.auth import get_user_model
from django.utils import timezone

from habits.models import Habit
from telegram_bot.services import send_telegram_message
from telegram_bot.tasks import (
    send_habit_reminders,
    send_telegram_message_task,
)


User = get_user_model()


@pytest.mark.django_db
def test_send_telegram_message_task():
    with patch(
        "telegram_bot.tasks.send_telegram_message"
    ) as mock_send:
        send_telegram_message_task(
            "12345",
            "Тестовое сообщение",
        )

        mock_send.assert_called_once_with(
            "12345",
            "Тестовое сообщение",
        )


@pytest.mark.django_db
def test_send_habit_reminders_with_telegram():
    user = User.objects.create_user(
        email="test@example.com",
        password="password",
        telegram_chat_id="12345",
    )

    current_time = timezone.localtime().time().replace(
        second=0,
        microsecond=0,
    )

    Habit.objects.create(
        user=user,
        place="Дом",
        time=current_time,
        action="Сделать зарядку",
        execution_time=60,
    )

    with patch(
        "telegram_bot.tasks.send_telegram_message_task.delay"
    ) as mock_task:

        send_habit_reminders()

        mock_task.assert_called_once_with(
            "12345",
            "Напоминание: Сделать зарядку",
        )


@pytest.mark.django_db
def test_send_habit_reminders_without_telegram():
    user = User.objects.create_user(
        email="test2@example.com",
        password="password",
    )

    current_time = timezone.localtime().time().replace(
        second=0,
        microsecond=0,
    )

    Habit.objects.create(
        user=user,
        place="Дом",
        time=current_time,
        action="Читать книгу",
        execution_time=60,
    )

    with patch(
        "telegram_bot.tasks.send_telegram_message_task.delay"
    ) as mock_task:

        send_habit_reminders()

        mock_task.assert_not_called()


def test_send_telegram_message_success(settings):
    settings.TELEGRAM_BOT_TOKEN = "test-token"

    response = Mock()
    response.json.return_value = {
        "ok": True,
    }

    with patch(
        "telegram_bot.services.requests.post",
        return_value=response,
    ):
        result = send_telegram_message(
            "12345",
            "Hello",
        )

    assert result == {
        "ok": True,
    }


def test_send_telegram_message_error(settings):
    settings.TELEGRAM_BOT_TOKEN = "test-token"

    with patch(
            "telegram_bot.services.requests.post",
            side_effect=requests.RequestException(
                "Connection error"),


    ):
        result = send_telegram_message(
            "12345",
            "Hello",
        )

    assert "error" in result

