"""
Подготовка клиента Redis.
"""

from dataclasses import dataclass

from app.infrastructure.settings.redis import RedisSettings


@dataclass(frozen=True)
class RedisConnectionInfo:
    url: str


def build_connection_info(settings: RedisSettings) -> RedisConnectionInfo:
    return RedisConnectionInfo(url=str(settings.url))
