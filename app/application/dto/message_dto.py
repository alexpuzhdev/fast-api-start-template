"""
DTO для передачи сообщения наружу.
"""

from pydantic import BaseModel


class MessageDTO(BaseModel):
    text: str
    source: str
