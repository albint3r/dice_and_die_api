from json import JSONDecodeError

from icecream import ic
from pydantic import BaseModel, ValidationError
from abc import ABC, abstractmethod

from starlette.websockets import WebSocket

from app.domain.auth.entities.user import User
from app.domain.core.ref_types import TGamePlayer
from app.domain.game.entities.game import Game
from app.domain.game.entities.game_config import GameConfig
from app.domain.game.entities.player import Player
from app.domain.game.enums.game_event import GameEvent
from app.domain.game.schemas.request import GamePlayerRequest
from app.domain.game.use_cases.i_game_websocket_manager import IGameWebSocketManager
from app.repositories.auth.auth_repository import AuthRepository


class IGamesModeRunner(BaseModel, ABC):
    config: GameConfig
    repo: AuthRepository
    ws_game: IGameWebSocketManager

    @abstractmethod
    async def play(self, game: Game, **kwargs) -> None:
        """Run the game depending on the game mode"""

    @abstractmethod
    async def create_or_join(self, game_id: str, user_id: str, websocket: WebSocket) -> TGamePlayer:
        """Player Create or join to an existed game."""

    @abstractmethod
    def create_new_game(self, game_id: str, player: Player) -> Game:  # noqa
        """Create a new Game."""

    @abstractmethod
    def create_new_player(self, user: User) -> Player:  # noqa
        """Create a new player from an existing user."""

    @abstractmethod
    def get_user(self, user_id: str) -> User:
        """Create an instance of the user by the user id"""
        user = self.repo.get_user_by_id(user_id)
        user.user_level = self.repo.get_user_level(user.user_id)
        user.bank_account = self.repo.get_user_bank_account(user.user_id)
        return user

    @abstractmethod
    def verbose(self, game: Game) -> None:  # noqa
        """Create an instance of the user by the user id"""
        ic('*-' * 100)
        ic(f'Current player: {game.current_player.user.name} | Die:{game.current_player.die.current_number}')
        ic(f'GameState: {game.state}')
        ic('*-' * 100)
        ic(f'Player 1:{game.p1.user.name}')
        ic(f'Board:{game.p1.board}')
        ic(f'Player 2:{game.p2.user.name}')
        ic(f'Board:{game.p2.board}')
        ic('*-' * 100)

    async def get_user_event_request(self, websocket: WebSocket) -> GamePlayerRequest:  # noqa
        """Get the player message event from the client"""
        try:
            json_str = await websocket.receive_json()
            return GamePlayerRequest(**json_str)
        except ValidationError:
            return GamePlayerRequest(event=GameEvent.INVALID_INPUT_EVENT)
        except JSONDecodeError:
            return GamePlayerRequest(event=GameEvent.INVALID_INPUT_EVENT)
