import os
import logging
import requests
from typing import NoReturn
from enum import Enum

logger = logging.getLogger(__name__)

class NotificationPriority(Enum):
    MAX = "max"
    HIGH = "high"
    DEFAuLT = "default"
    LOW = "low"
    MIN = "min"


def _notify(
    topic: str,
    content: str,
    priority: NotificationPriority = NotificationPriority.DEFAuLT,
    tags: str = "",
    click: str = "",
    email: str = "",
    host: str = "ntfy.sh",
) -> NoReturn:
    requests.post(
        f"https://{host}/{topic}",
        data=content,
        headers={
            "X-Priority": priority.value,
            "X-Tags": tags,
            "X-Click": click,
            "X-Email": email,
        },
    )

def notify(old_value: str, new_value: str, url: str, watch_name: str):
    email = os.getenv("NOTIFICATION_EMAIL")
    if not email:
        logger.warning("Email not set")
    topic = os.getenv("NTFY_TOPIC")
    if not topic:
        logger.error("No ntfy topic set")
        return

    message = f"Your watched content \"{watch_name}\" has changed from {old_value} to {new_value}"
    _notify(
        topic=topic,
        content=message,
        click=url,
        email=email
    )