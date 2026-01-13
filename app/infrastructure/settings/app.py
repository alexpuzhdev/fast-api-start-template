"""
Настройки приложения.
"""

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from app.infrastructure.settings.base import BaseAppSettings
from app.infrastructure.settings.database import DatabaseSettings
from app.infrastructure.settings.redis import RedisSettings


class AppSettings(BaseAppSettings):
    name: str = Field(default="FastAPI Clean Template", validation_alias="APP_NAME")
    environment: str = Field(default="local", validation_alias="APP_ENV")
    debug: bool = Field(default=False, validation_alias="APP_DEBUG")
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


def load_settings() -> AppSettings:
    """
    Явно загружает настройки приложения.
    """
    return AppSettings()
