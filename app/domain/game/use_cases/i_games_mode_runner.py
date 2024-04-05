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
from app.domain.game.use_cases.i_user_level_use_case import IManagerLevelingUseCase
from app.domain.game.use_cases.i_viewers_websocket_manager import IViewersWebSocketManager
from app.repositories.auth.auth_repository import AuthRepository


class IGamesModeRunner(BaseModel, ABC):
    config: GameConfig
    repo: AuthRepository
    ws_game: IGameWebSocketManager
    ws_viewers: IViewersWebSocketManager
    leveling_manager: IManagerLevelingUseCase

    @abstractmethod
    async def play(self, game: Game,
                   player: Player | None = None,
                   game_events: GamePlayerRequest | None = None,
                   **kwargs) -> None:
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
        ic('/' * 100)
        ic(f'Current player: {game.current_player.user.name} | Die:{game.current_player.die.current_number}')
        ic(f'GameState: {game.state}')
        ic('/' * 100)
        ic(f'Player 2:{game.p2.user.name}')
        ic(game.p2.board.columns.get(1), game.p2.board.columns.get(2), game.p2.board.columns.get(3))
        ic('.' * 100)
        ic(f'Player 1:{game.p1.user.name}')
        ic(game.p1.board.columns.get(1), game.p1.board.columns.get(2), game.p1.board.columns.get(3))
        ic('*-' * 100)

    @abstractmethod
    def select_column(self, request: GamePlayerRequest) -> int:
        try:
            return int(request.event.value)
        except ValueError:
            return 0

    def update_player_scores(self, game: Game) -> None:  # noqa
        """Update the player score after each move."""

    @abstractmethod
    async def get_winner_after_player_disconnect(self, disconnected_player: Player, game: Game,
                                                 websocket: WebSocket) -> None:
        """Get the winner after a user disconnect before the game ends."""

    async def get_user_event_request(self, websocket: WebSocket) -> GamePlayerRequest:  # noqa
        """Get the player message event from the client"""
        try:
            json_str = await websocket.receive_json()
            return GamePlayerRequest(**json_str)
        except ValidationError:
            return GamePlayerRequest(event=GameEvent.INVALID_INPUT_EVENT)
        except JSONDecodeError:
            return GamePlayerRequest(event=GameEvent.INVALID_INPUT_EVENT)
