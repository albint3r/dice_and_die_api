from abc import ABC, abstractmethod

from pydantic import BaseModel
from starlette.websockets import WebSocket

from app.domain.game.use_cases.i_game_websocket_manager import IGameWebSocketManager
from app.domain.core.ref_types import TGamePlayer
from app.domain.game.entities.game import Game
from app.domain.game.entities.player import Player
from app.domain.game.schemas.request import GamePlayerRequest
from app.domain.game.use_cases.i_user_level_use_case import IManagerLevelingUseCase
from app.repositories.auth.auth_repository import AuthRepository


class IGameUseCase(BaseModel, ABC):
    websocket_manager: IGameWebSocketManager
    leveling_manager: IManagerLevelingUseCase
    repo: AuthRepository

    @abstractmethod
    async def execute(self, game: Game):
        """Depends on the [GameState] execute a function that provide the values to continue the [game] flow"""

    @abstractmethod
    async def create_or_join_game(self, game_id: str, user_id: str, websocket: WebSocket) -> TGamePlayer:
        """Player Create or join to an existed game."""

    @abstractmethod
    async def get_player_request_event(self, websocket: WebSocket) -> GamePlayerRequest:
        """Get the player message event from the client"""

    @abstractmethod
    async def get_winner_after_player_disconnect(self, disconnected_player: Player, game: Game,
                                                 websocket: WebSocket) -> None:
        """Get the winner after a user disconnect before the game ends."""
