from starlette.websockets import WebSocket

from app.domain.core.i_websocket_manager import IWebSocketManager
from app.domain.core.ref_types import TActiveConnectionsViewers, TExtras
from abc import ABC, abstractmethod

from app.domain.game.entities.game import Game


class IViewersWebSocketManager(IWebSocketManager, ABC):
    active_connections: TActiveConnectionsViewers = {}

    @abstractmethod
    async def connect(self, game_id: str, websocket: WebSocket) -> None:
        """Connect viewer to watch the match"""

    @abstractmethod
    async def disconnect(self, game_id: str, websocket: WebSocket) -> None:
        """Disconnect viewer of the match"""

    @abstractmethod
    async def broadcast(self, game: Game, message: str = '', extras: TExtras | None = None) -> None:
        """Broadcast Cheering to the players"""
