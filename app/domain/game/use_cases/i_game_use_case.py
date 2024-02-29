from abc import ABC, abstractmethod

from pydantic import BaseModel
from starlette.websockets import WebSocket

from app.domain.auth.entities.user import User
from app.domain.core.ref_types import TGamePlayer
from app.domain.game.entities.game import Game
from app.domain.game.entities.player import Player
from app.domain.game.schemas.request import GamePlayerRequest
from app.domain.game.use_cases.i_game_websocket_manager import IGameWebSocketManager
from app.domain.game.use_cases.i_user_level_use_case import IManagerLevelingUseCase
from app.domain.game.use_cases.i_viewers_websocket_manager import IViewersWebSocketManager
from app.repositories.auth.auth_repository import AuthRepository


class IGameUseCase(BaseModel, ABC):
    websocket_manager: IGameWebSocketManager
    viewers_websocket_manager: IViewersWebSocketManager
    leveling_manager: IManagerLevelingUseCase
    repo: AuthRepository

    @abstractmethod
    async def execute(self, game: Game):
        """Depends on the [GameState] execute a function that provide the values to continue the [game] flow"""

    @abstractmethod
    async def create_or_join(self, game_id: str, user_id: str, websocket: WebSocket) -> TGamePlayer:
        """Player Create or join to an existed game."""

    @abstractmethod
    async def get_user_request_event(self, websocket: WebSocket) -> GamePlayerRequest:
        """Get the player message event from the client"""

    @abstractmethod
    async def get_winner_after_player_disconnect(self, disconnected_player: Player, game: Game,
                                                 websocket: WebSocket) -> None:
        """Get the winner after a user disconnect before the game ends."""

    @abstractmethod
    def get_valid_game_id(self, user_id: str, game_id: str) -> str:
        """Validate if the user is already in the match.
        This avoids bugs and player play with him self.
        """
