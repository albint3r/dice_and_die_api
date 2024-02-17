from abc import ABC, abstractmethod


class BaseWebSocketManager(ABC):
    """Clase base para manejar WebSockets."""

    @abstractmethod
    async def connect(self, *args, **kwargs) -> None:
        """Método por defecto para conectar."""

    @abstractmethod
    async def disconnect(self, *args, **kwargs) -> None:
        """Método por defecto para desconectar."""

    @abstractmethod
    async def broadcast(self, *args, **kwargs) -> None:
        """Método por defecto para transmitir."""
