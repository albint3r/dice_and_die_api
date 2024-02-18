from random import choice

from starlette.websockets import WebSocket

from app.domain.auth.entities.user import User
from app.domain.core.ref_types import TGamePlayer
from app.domain.game.entities.board import Board
from app.domain.game.entities.column import Column
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

    def _get_starter_player(self, game: Game) -> Player:  # noqa
        """Select randomly witch player would start the game."""
        return choice([game.p1, game.p2])

    def _select_column(self, request: GamePlayerRequest) -> int:  # noqa
        """Convert the event string in a number column index. In case is not a valid number return [False]"""
        try:
            return int(request.event.value)
        except ValueError:
            return False

    async def execute(self, game: Game, **kwargs):
        match game.state:
            case GameState.CREATE_NEW_GAME:
                game.state = GameState.WAITING_OPPONENT
                await self.websocket_manager.broadcast(game_id=game.game_id,
                                                       message='Player 1 Connected',
                                                       extras={})
            case GameState.WAITING_OPPONENT:
                started_player = self._get_starter_player(game)
                game.current_player = started_player
                game.state = GameState.ROLL_DICE
                await self.websocket_manager.broadcast(game_id=game.game_id,
                                                       message='Player 2 Connected',
                                                       extras={})
            case GameState.ROLL_DICE:
                game.current_player.die.roll()
                game.state = GameState.SELECT_COLUMN
                await self.websocket_manager.broadcast(game_id=game.game_id,
                                                       message=f'User {game.current_player} roll dice',
                                                       extras={})
            case GameState.SELECT_COLUMN:
                request: GamePlayerRequest = kwargs['selected_column']
                column_index = self._select_column(request.event.value)
                column = game.current_player.board.columns.get(column_index)
                if column_index and not column.is_full():
                    game.state = GameState.ADD_DICE_TO_COLUMN
                    await self.execute(game, column_index=column_index)

            case GameState.ADD_DICE_TO_COLUMN:
                column_index: int = kwargs['column_index']
                column = game.current_player.board.columns.get(column_index)
                die_val = game.current_player.die.current_number
                column.add(die_val)
                opponent_player = game.get_opponent_player()
                column_opponent_player = opponent_player.board.columns.get(column_index)
                if column_opponent_player.can_remove_values(die_val):
                    game.state = GameState.DESTROY_OPPONENT_TARGET_COLUMN
                    await self.execute(game, column_opponent_player=column_opponent_player, die_val=die_val)
                else:
                    game.state = GameState.UPDATE_PLAYERS_POINTS
                    await self.websocket_manager.broadcast(game_id=game.game_id,
                                                           message='add_dice_to_colum',
                                                           extras={})
            case GameState.DESTROY_OPPONENT_TARGET_COLUMN:
                column_opponent_player: Column = kwargs['column_opponent_player']
                die_val: int = kwargs['die_val']
                removed_indices = column_opponent_player.remove(die_val)
                game.state = GameState.UPDATE_PLAYERS_POINTS
                await self.websocket_manager.broadcast(game_id=game.game_id,
                                                       message='destroy_opponent_target_column',
                                                       extras={'removed_indices': removed_indices})

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
        json_str = await websocket.receive_json()
        return GamePlayerRequest(**json_str)
