from abc import ABC, abstractmethod

from starlette.websockets import WebSocket

from app.domain.core.base_websocket_manager import BaseWebSocketManager
from app.domain.core.ref_types import TActiveConnections, TActiveGames, TExtras
from app.domain.game.entities.game import Game


class IGameWebSocketManager(BaseWebSocketManager, ABC):
    """This class handle the websocket game services"""
    active_connections: TActiveConnections = {}
    active_games: TActiveGames = {}

    @abstractmethod
    async def connect(self, game_id: str, new_game: Game, websocket: WebSocket) -> None:
        """Add user websocket to active connection and add game to active games if not exist."""

    @abstractmethod
    async def disconnect(self, game_id: str, websocket: WebSocket) -> None:
        """Disconnect player from the room. Remove the game if one of the players left the match.
        This have a conditional, because the remaining player could trigger this event, this check
        if the game already exist to be eliminated.
        """

    @abstractmethod
    async def broadcast(self, game_id: str, message: str = '', extras: TExtras | None = None) -> None:
        """Broadcast the game to all the players and viewers that are listening the websocket"""

    @abstractmethod
    def get_remained_player_websocket(self, game_id: str) -> WebSocket:
        """Return the Remained player. This is useful after a user disconnect from the match"""