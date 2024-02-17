from abc import ABC, abstractmethod

from pydantic import BaseModel
from starlette.websockets import WebSocket

from app.domain.core.i_game_websocket_manager import IGameWebSocketManager
from app.domain.core.ref_types import TGamePlayer
from app.domain.game.entities.game import Game
from app.domain.game.schemas.request import GamePlayerRequest


class IGameUseCase(BaseModel, ABC):
    websocket_manager: IGameWebSocketManager

    @abstractmethod
    def execute(self, game: Game):
        """Depends on the [GameState] execute a function that provide the values to continue the [game] flow"""

    @abstractmethod
    async def create_or_join_game(self, game_id: str, user_id: str, websocket: WebSocket) -> TGamePlayer:
        """Player Create or join to an existed game."""

    @abstractmethod
    def get_player_request_event(self) -> GamePlayerRequest:
        """Get the player message event from the client"""
