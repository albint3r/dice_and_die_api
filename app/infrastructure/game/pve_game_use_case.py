import uuid
from json import JSONDecodeError
from random import choice

from icecream import ic
from pydantic import ValidationError
from starlette.websockets import WebSocket

from app.domain.analytics.entities.single_play_history import SinglePlayHistory
from app.domain.core.ref_types import TGamePlayer
from app.domain.game.entities.board import Board
from app.domain.game.entities.column import Column
from app.domain.game.entities.die import Die
from app.domain.game.entities.game import Game
from app.domain.game.entities.player import Player
from app.domain.game.entities.player_rol import PlayerRol
from app.domain.game.enums.game_event import GameEvent
from app.domain.game.enums.game_state import GameState
from app.domain.game.schemas.request import GamePlayerRequest
from app.domain.game.use_cases.i_game_use_case import IGameUseCase
from app.domain.game.use_cases.i_game_websocket_manager import IGameWebSocketManager
from app.repositories.auth.auth_repository import AuthRepository
from app.domain.auth.entities.user import User


class PVEGameUseCase(IGameUseCase):
    websocket_manager: IGameWebSocketManager
    repo: AuthRepository

    def _get_starter_player(self, game: Game) -> Player:  # noqa
        """Select randomly witch player would start the game."""
        return game.p1

    def _get_user(self, user_id: str) -> User:
        """Create an instance of the user by the user id"""
        user = self.repo.get_user_by_id(user_id)
        user.user_level = self.repo.get_user_level(user.user_id)
        user.bank_account = self.repo.get_user_bank_account(user.user_id)
        return user

    def _create_new_player(self, user: User) -> Player:  # noqa
        """Create a new player from an existing user."""
        return Player(user=user, board=Board(), die=Die())

    def _create_new_game(self, game_id: str, player: Player, player_ai: Player) -> Game:  # noqa
        """Create a new Game."""
        return Game(game_id=game_id, p1=player, p2=player_ai, state=GameState.WAITING_OPPONENT)

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

    async def create_or_join(self, game_id: str, user_id: str, websocket: WebSocket) -> TGamePlayer:
        """Create a room for the player and an AI."""
        player = self._create_new_player(self._get_user(user_id))
        player_ai = self._create_new_player(self._get_user('I007'))
        player_ai.rol = PlayerRol.AI
        game = self._create_new_game(game_id, player, player_ai)
        await self.websocket_manager.connect(game_id=game_id, new_game=game, websocket=websocket)
        return game, player

    async def get_user_request_event(self, websocket: WebSocket) -> GamePlayerRequest:
        try:
            json_str = await websocket.receive_json()
            return GamePlayerRequest(**json_str)
        except ValidationError:
            return GamePlayerRequest(event=GameEvent.INVALID_INPUT_EVENT)
        except JSONDecodeError:
            return GamePlayerRequest(event=GameEvent.INVALID_INPUT_EVENT)

    async def get_winner_after_player_disconnect(self, disconnected_player: Player, game: Game,
                                                 websocket: WebSocket) -> None:
        pass

    def get_valid_game_id(self, _: str, __: str) -> str:
        return str(uuid.uuid4())

    def _update_player_scores(self, game: Game) -> None:  # noqa
        """Update the current players scores"""
        game.p1.board.get_score()
        game.p2.board.get_score()

    def _select_column(self, request: GamePlayerRequest) -> int:  # noqa
        """Convert the event string in a number column index. In case is not a valid number return [False]"""
        try:
            return int(request.event.value)
        except ValueError:
            return 0

    def _save_single_game_history(self, game: Game, column_index: int) -> None:
        """Save single game history player column selection"""
        single_game_history = SinglePlayHistory.from_game(game, column_index)
        self.repo.save_single_play_history(single_game_history)

    def get_ai_selected_column(self, game: Game) -> str:
        """Return the index integer of the column to select by the AI"""
        columns = game.p2.board.columns
        available_columns = [str(i) for i, col in columns.items() if not col.is_full()]
        return choice(available_columns)

    async def execute(self, game: Game, **kwargs):
        match game.state:
            case GameState.WAITING_OPPONENT:
                started_player = self._get_starter_player(game)
                game.current_player = started_player
                game.state = GameState.ROLL_DICE
                extras = {}
                message = 'player_2_connected'
                await self.websocket_manager.broadcast(game_id=game.game_id, message=message, extras=extras)

            case GameState.ROLL_DICE:
                game.current_player.die.roll()
                game.state = GameState.SELECT_COLUMN
                extras = {}
                message = 'roll_dice'
                await self.websocket_manager.broadcast(game_id=game.game_id, message=message, extras=extras)

            case GameState.SELECT_COLUMN:
                request: GamePlayerRequest = kwargs['selected_column']
                column_index = self._select_column(request)
                column = game.current_player.board.columns.get(column_index)
                # Only save the user movement and not the AI.
                if column_index and not column.is_full():
                    # This save the result move from the user. This table helps to the machine learning model.
                    if game.current_player == game.p1:
                        self._save_single_game_history(game, column_index)
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
                    extras = {}
                    message = 'add_dice'
                    await self.websocket_manager.broadcast(game_id=game.game_id, message=message, extras=extras)
                    await self.execute(game)

            case GameState.DESTROY_OPPONENT_TARGET_COLUMN:
                column_opponent_player: Column = kwargs['column_opponent_player']
                die_val: int = kwargs['die_val']
                removed_indices = column_opponent_player.remove(die_val)
                game.state = GameState.UPDATE_PLAYERS_POINTS
                extras = {'removed_indices': removed_indices}
                message = 'destroy_opponent_target_column'
                await self.websocket_manager.broadcast(game_id=game.game_id, message=message, extras=extras)
                await self.execute(game)

            case GameState.UPDATE_PLAYERS_POINTS:
                self._update_player_scores(game)
                if game.is_finished:
                    game.state = GameState.FINISH_GAME
                else:
                    game.state = GameState.CHANGE_CURRENT_PLAYER
                extras = {}
                message = 'update_players_points'
                await self.websocket_manager.broadcast(game_id=game.game_id, message=message, extras=extras)

            case GameState.CHANGE_CURRENT_PLAYER:
                game.current_player = game.get_opponent_player()
                game.state = GameState.ROLL_DICE
                extras = {}
                message = 'change_current_player'
                await self.websocket_manager.broadcast(game_id=game.game_id, message=message, extras=extras)

            case GameState.FINISH_GAME:
                winner_player, tied_player = game.get_winner()
                exp_points = self.leveling_manager.get_winner_earned_exp_points(game)
                if tied_player:
                    # Update both players points and ranks
                    self._update_user_level_rank_and_bank_account(exp_points, tied_player)
                self._update_user_level_rank_and_bank_account(exp_points, winner_player)
                extras = {}
                message = 'finish_game'
                await self.websocket_manager.broadcast(game_id=game.game_id, message=message, extras=extras)
                self.save_game_history(game)

            case GameState.DISCONNECT_PLAYER:
                winner_player, _ = game.winner_player
                exp_points = self.leveling_manager.get_winner_earned_exp_after_player_disconnect()
                # Create a copy to compare if the user level up
                self._update_user_level_rank_and_bank_account(exp_points, winner_player)
                extras = {}
                message = 'player_disconnected'
                await self.websocket_manager.broadcast(game_id=game.game_id, message=message, extras=extras)
                await self.viewers_websocket_manager.broadcast(game=game, message=message, extras=extras)
