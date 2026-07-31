import requests
from django.conf import settings


def send_telegram_message(chat_id, message):
    url = (
        f"https://api.telegram.org/"
        f"bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    )

    response = requests.post(
        url,
        data={
            "chat_id": chat_id,
            "text": message,
        },
        timeout=10,
    )

    response.raise_for_status()

    return response.json()
