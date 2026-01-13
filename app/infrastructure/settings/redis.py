"""
Настройки Redis.
"""

from pydantic import RedisDsn
from pydantic_settings import SettingsConfigDict

from app.infrastructure.settings.base import BaseAppSettings


class RedisSettings(BaseAppSettings):
    url: RedisDsn

    model_config = SettingsConfigDict(
        env_prefix="REDIS_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
