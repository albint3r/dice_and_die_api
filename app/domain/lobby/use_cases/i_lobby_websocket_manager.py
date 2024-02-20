from abc import ABC, abstractmethod

from starlette.websockets import WebSocket

from app.domain.game.use_cases.i_websocket_manager import IWebSocketManager
from app.domain.core.ref_types import TActiveGames, TLobbyActiveConnections


class ILobbyWebSocketManager(IWebSocketManager, ABC):
    """This is the Base Class to the Lobby WebSockets Manager"""
    active_connections: TLobbyActiveConnections = []

    @abstractmethod
    async def connect(self, websocket: WebSocket) -> None:
        """Connect User to pool connections"""

    @abstractmethod
    async def disconnect(self, websocket: WebSocket) -> None:
        """Disconnect user from pool connections"""

    @abstractmethod
    async def broadcast(self, active_games: TActiveGames) -> None:
        """Broadcast when a new user is connected in the lobby"""

    @abstractmethod
    def get_total_connected_users(self) -> int:
        """Get the total connect users"""
