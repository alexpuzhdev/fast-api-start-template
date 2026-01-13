"""
Доменная сущность сообщения.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Message:
    text: str
    source: str
