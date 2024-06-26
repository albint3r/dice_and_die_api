from abc import ABC, abstractmethod

from pydantic import BaseModel
from starlette.websockets import WebSocket

from app.domain.game.use_cases.i_game_websocket_manager import IGameWebSocketManager
from app.domain.lobby.schemas.request import LobbyEventRequest
from app.domain.lobby.use_cases.i_lobby_websocket_manager import ILobbyWebSocketManager


class ILobbyUseCase(BaseModel, ABC):
    """This is the Lobby UseCase"""
    game_websocket_manager: IGameWebSocketManager
    lobby_websocket_manager: ILobbyWebSocketManager

    @abstractmethod
    async def subscribe_user(self, user_id: str, websocket: WebSocket) -> None:
        """Connect user to the lobby pool connections"""

    @abstractmethod
    async def unsubscribe_user(self, user_id: str, websocket: WebSocket) -> None:
        """Disconnect user from the lobby pool connections"""

    @abstractmethod
    async def update_lobby_information(self) -> None:
        """Broadcast the games to connected users"""

    @abstractmethod
    async def get_player_request_event(self, user_id: str, websocket: WebSocket) -> LobbyEventRequest:
        """Broadcast the games to connected users"""
