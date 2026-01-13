"""
Схемы для сообщений.
"""

from pydantic import BaseModel


class MessageResponse(BaseModel):
    text: str
    source: str
