"""
Зависимости контейнера.
"""

from app.container import Container

_container_instance: Container | None = None


def get_container() -> Container:
    """
    Возвращает singleton контейнера.
    """
    global _container_instance
    if _container_instance is None:
        _container_instance = Container()
    return _container_instance
