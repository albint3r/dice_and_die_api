from starlette.websockets import WebSocket

from app.domain.auth.entities.user import User
from app.domain.core.ref_types import TGamePlayer
from app.domain.game.entities.board import Board
from app.domain.game.entities.column import Column
from app.domain.game.entities.die import Die
from app.domain.game.entities.game import Game
from app.domain.game.entities.player import Player
from app.domain.game.enums.game_state import GameState
from app.domain.game.use_cases.i_games_mode_runner import IGamesModeRunner


class AdventureGameModeRunner(IGamesModeRunner):
    async def play(self, game: Game, **kwargs) -> None:
        pass

    async def create_or_join(self, game_id: str, user_id: str, websocket: WebSocket) -> TGamePlayer:
        game = self.ws_game.active_games.get(game_id)
        if not game:
            player = self.create_new_player(self.get_user(user_id))
            game = self.create_new_game(game_id, player)
            await self.ws_game.connect(game_id=game_id, new_game=game, websocket=websocket)
        else:
            player = self.create_new_player(self.get_user(user_id))
            game.p2 = player
            await self.ws_game.connect(game_id=game_id, new_game=game, websocket=websocket)

        return game, player

    def create_new_game(self, game_id: str, player: Player) -> Game:
        return Game(game_id=game_id, p1=player, state=GameState.CREATE_NEW_GAME)

    def create_new_player(self, user: User) -> Player:
        return Player(
            user=user,
            board=self._create_board(),
            die=Die()
        )

    def get_user(self, user_id: str) -> User:
        return super().get_user(user_id)

    def verbose(self, game: Game) -> None:
        super().verbose(game)

    def _create_board(self, max_length: int = 4) -> Board:  # noqa
        return Board(
            columns={1: Column(max_length=max_length),
                     2: Column(max_length=max_length),
                     3: Column(max_length=max_length),
                     4: Column(max_length=max_length)}
        )
