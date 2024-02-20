from abc import ABC, abstractmethod

from pydantic import BaseModel


class IWebSocketManager(BaseModel, ABC):
    """Clase base para manejar WebSockets."""

    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    async def connect(self, *args, **kwargs) -> None:
        """Método por defecto para conectar."""

    @abstractmethod
    async def disconnect(self, *args, **kwargs) -> None:
        """Método por defecto para desconectar."""

    @abstractmethod
    async def broadcast(self, *args, **kwargs) -> None:
        """Método por defecto para transmitir."""
