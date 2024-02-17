import pytest
from icecream import ic
from starlette.websockets import WebSocket

from app.domain.auth.entities.user import User
from app.domain.core.ref_types import TGamePlayer
from app.domain.game.entities.board import Board
from app.domain.game.entities.die import Die
from app.domain.game.entities.game import Game
from app.domain.game.entities.player import Player
from app.domain.game.enums.game_state import GameState
from app.domain.game.schemas.request import GamePlayerRequest
from app.domain.game.use_cases.i_game_use_case import IGameUseCase
from app.test.utils import create_fake_p1, create_fake_p2


class GameUseCase(IGameUseCase):

    def _create_new_player(self, user: User) -> Player:  # noqa
        """Create a new player from an existing user."""
        return Player(user=user, board=Board(), die=Die())

    def _create_new_game(self, game_id: str, player: Player) -> Game:  # noqa
        """Create a new Game."""
        return Game(game_id=game_id, p1=player, state=GameState.CREATE_NEW_GAME)

    async def execute(self, game: Game):
        match game.state:
            case GameState.CREATE_NEW_GAME:
                game.state = GameState.WAITING_OPPONENT
                await self.websocket_manager.broadcast(game_id=game.game_id,
                                                       message='Player 1 Connected',
                                                       extras={})

    async def create_or_join_game(self, game_id: str, user_id: str, websocket: WebSocket) -> TGamePlayer:
        game = self.websocket_manager.active_games.get(game_id)
        if not game:
            player = self._create_new_player(create_fake_p1())
            game = self._create_new_game(game_id, player)
            await self.websocket_manager.connect(game_id=game_id, new_game=game, websocket=websocket)
        else:
            player = self._create_new_player(create_fake_p2())
            game.p2 = player
            await self.websocket_manager.connect(game_id=game_id, new_game=game, websocket=websocket)

        return game, player

    async def get_player_request_event(self, websocket: WebSocket) -> GamePlayerRequest:
        import json
        json_str = await websocket.receive_json()
        json_data = json.loads(json_str)
        return GamePlayerRequest(**json_data)
