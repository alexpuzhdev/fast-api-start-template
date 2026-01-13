"""
Контейнер зависимостей приложения.
"""

from app.application.use_cases.get_message import GetMessageUseCase
from app.infrastructure.repositories.static_message_repository import StaticMessageRepository
from app.infrastructure.settings.app import AppSettings, load_settings


class Container:
    def __init__(self) -> None:
        self._settings = load_settings()
        self._message_repository = StaticMessageRepository(
            message_text="FastAPI clean architecture template",
            message_source=self._settings.name,
        )
        self._get_message_use_case = GetMessageUseCase(self._message_repository)

    @property
    def settings(self) -> AppSettings:
        return self._settings

    @property
    def get_message_use_case(self) -> GetMessageUseCase:
        return self._get_message_use_case
