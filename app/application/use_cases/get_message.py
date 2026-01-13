"""
Use case получения сообщения.
"""

from app.application.dto.message_dto import MessageDTO
from app.domain.repositories.message_repository import MessageRepository


class GetMessageUseCase:
    def __init__(self, message_repository: MessageRepository) -> None:
        self._message_repository = message_repository

    def execute(self) -> MessageDTO:
        message = self._message_repository.get_message()
        return MessageDTO(text=message.text, source=message.source)
