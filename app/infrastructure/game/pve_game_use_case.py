from starlette.websockets import WebSocket

from app.domain.core.ref_types import TGamePlayer
from app.domain.game.entities.board import Board
from app.domain.game.entities.die import Die
from app.domain.game.entities.game import Game
from app.domain.game.entities.player import Player
from app.domain.game.enums.game_state import GameState
from app.domain.game.schemas.request import GamePlayerRequest
from app.domain.game.use_cases.i_game_use_case import IGameUseCase
from app.domain.game.use_cases.i_game_websocket_manager import IGameWebSocketManager
from app.repositories.auth.auth_repository import AuthRepository


class PVEGameUseCase(IGameUseCase):
    websocket_manager: IGameWebSocketManager
    repo: AuthRepository

    def _create_new_player(self, user: User) -> Player:  # noqa
        """Create a new player from an existing user."""
        return Player(user=user, board=Board(), die=Die())


    def _create_new_game(self, game_id: str, player: Player) -> Game:  # noqa
        """Create a new Game."""
        return Game(game_id=game_id, p1=player, state=GameState.CREATE_NEW_GAME)

    async def create_or_join(self, game_id: str, user_id: str, websocket: WebSocket) -> TGamePlayer:
        """Create a room for the player and an AI."""
        player = self._create_new_player(self._get_user(user_id))
        game = self._create_new_game(game_id, player)
        await self.websocket_manager.connect(game_id=game_id, new_game=game, websocket=websocket)

    async def execute(self, game: Game):
        pass

    async def get_user_request_event(self, websocket: WebSocket) -> GamePlayerRequest:
        pass

    async def get_winner_after_player_disconnect(self, disconnected_player: Player, game: Game,
                                                 websocket: WebSocket) -> None:
        pass

    def get_valid_game_id(self, user_id: str, game_id: str) -> str:
        pass
