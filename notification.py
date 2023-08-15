import requests
from typing import NoReturn
from enum import Enum


class NotificationPriority(Enum):
    MAX = "max"
    HIGH = "high"
    DEFAuLT = "default"
    LOW = "low"
    MIN = "min"


def notify(
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