from json import JSONDecodeError
from random import choice

from icecream import ic
from pydantic import ValidationError
from starlette.websockets import WebSocket

from app.domain.auth.entities.user import User
from app.domain.core.ref_types import TGamePlayer
from app.domain.game.entities.board import Board
from app.domain.game.entities.column import Column
from app.domain.game.entities.die import Die
from app.domain.game.entities.game import Game
from app.domain.game.entities.player import Player
from app.domain.game.enums.game_event import GameEvent
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
        ic(request)
        try:
            return int(request.event.value)
        except ValueError:
            return 0

    def _update_player_scores(self, game: Game) -> None:  # noqa
        """Update the current players scores"""
        game.p1.board.get_score()
        game.p2.board.get_score()

    def verbose(self, game) -> None:  # noqa
        ic('*-' * 100)
        ic(f'Current player: {game.current_player.user.name} | Die:{game.current_player.die.current_number}')
        ic(f'GameState: {game.state}')
        ic('*-' * 100)
        ic(f'Player 1:{game.p1.user.name}')
        ic(f'Board:{game.p1.board}')
        ic(f'Player 2:{game.p2.user.name}')
        ic(f'Board:{game.p2.board}')
        ic('*-' * 100)

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
        try:
            json_str = await websocket.receive_json()
            return GamePlayerRequest(**json_str)
        except ValidationError:
            return GamePlayerRequest(event=GameEvent.INVALID_INPUT_EVENT)
        except JSONDecodeError:
            return GamePlayerRequest(event=GameEvent.INVALID_INPUT_EVENT)

    async def get_winner_after_player_disconnect(self,
                                                 disconnected_player: Player,
                                                 game: Game,
                                                 websocket: WebSocket) -> None:
        # To avoid errors check if is not a winner and player 2 exist. Without this is not necessary
        # to give it the winne point.
        if not game.winner_player and game.p2:
            await self.websocket_manager.disconnect(game_id=game.game_id, websocket=websocket)
            connection = self.websocket_manager.get_remained_player_websocket(game.game_id)
            if connection:
                game.winner_player = (game.p1, None) if disconnected_player is game.p2 else (game.p2, None)
                game.state = GameState.DISCONNECT_PLAYER
                await self.execute(game)
        # If is not opponent disconnect safe.
        else:
            await self.websocket_manager.disconnect(game_id=game.game_id, websocket=websocket)

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
                column_index = self._select_column(request)
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
                    await self.execute(game,
                                       column_opponent_player=column_opponent_player,
                                       die_val=die_val)
                else:
                    game.state = GameState.UPDATE_PLAYERS_POINTS
                    await self.websocket_manager.broadcast(game_id=game.game_id,
                                                           message='add_dice_to_colum',
                                                           extras={})
                    await self.execute(game)

            case GameState.DESTROY_OPPONENT_TARGET_COLUMN:
                column_opponent_player: Column = kwargs['column_opponent_player']
                die_val: int = kwargs['die_val']
                removed_indices = column_opponent_player.remove(die_val)
                game.state = GameState.UPDATE_PLAYERS_POINTS
                await self.websocket_manager.broadcast(game_id=game.game_id,
                                                       message='destroy_opponent_target_column',
                                                       extras={'removed_indices': removed_indices})
                await self.execute(game)
            case GameState.UPDATE_PLAYERS_POINTS:
                self._update_player_scores(game)
                if game.is_finished:
                    game.state = GameState.FINISH_GAME
                else:
                    game.state = GameState.CHANGE_CURRENT_PLAYER
                await self.websocket_manager.broadcast(game_id=game.game_id,
                                                       message='update_players_points',
                                                       extras={})

            case GameState.CHANGE_CURRENT_PLAYER:
                game.current_player = game.get_opponent_player()
                game.state = GameState.ROLL_DICE
                await self.websocket_manager.broadcast(game_id=game.game_id,
                                                       message='update_players_points',
                                                       extras={})

            case GameState.FINISH_GAME:
                winner_player, tied_player = game.get_winner()
                exp_points = self.leveling_manager.get_winner_earned_exp_points(game)
                if tied_player:
                    # Update both players points and ranks
                    # Todo: Use this tied user to add to the repository
                    tied_user = self.leveling_manager.update_user_level(tied_player.user, exp_points)
                winner_user = self.leveling_manager.update_user_level(winner_player.user, exp_points)
                # Todo: Update the user rank and level in the Repository
                game.winner_player = winner_player, tied_player
                await self.websocket_manager.broadcast(game_id=game.game_id,
                                                       message='finish_game',
                                                       extras={})
            case GameState.DISCONNECT_PLAYER:
                winner_player, _ = game.winner_player
                exp_points = self.leveling_manager.get_winner_earned_exp_after_player_disconnect()
                # todo: still need to save the win exp in the db
                user = self.leveling_manager.update_user_level(winner_player.user, exp_points)
                await self.websocket_manager.broadcast(game_id=game.game_id,
                                                       message='player_disconnected_with_out_finished_the_game',
                                                       extras={})
