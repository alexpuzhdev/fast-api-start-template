"""
Пример инфраструктурной реализации репозитория.
"""

from app.domain.entities.message import Message
from app.domain.repositories.message_repository import MessageRepository


class StaticMessageRepository(MessageRepository):
    def __init__(self, message_text: str, message_source: str) -> None:
        self._message_text = message_text
        self._message_source = message_source

    def get_message(self) -> Message:
        return Message(text=self._message_text, source=self._message_source)
