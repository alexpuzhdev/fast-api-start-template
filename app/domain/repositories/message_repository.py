"""
Интерфейс репозитория сообщений.
"""

from typing import Protocol

from app.domain.entities.message import Message


class MessageRepository(Protocol):
    def get_message(self) -> Message:
        """
        Возвращает сообщение.
        """
