import copy
import uuid
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
from app.domain.game.entities.play_history import PlayHistory
from app.domain.game.entities.player import Player
from app.domain.analytics.entities.single_play_history import SinglePlayHistory
from app.domain.game.entities.player_rol import PlayerRol
from app.domain.game.enums.game_event import GameEvent
from app.domain.game.enums.game_state import GameState
from app.domain.game.schemas.request import GamePlayerRequest
from app.domain.game.use_cases.i_game_use_case import IGameUseCase
from fastapi import WebSocketException, status

from app.domain.game.use_cases.i_game_websocket_manager import IGameWebSocketManager
from app.domain.game.use_cases.i_user_level_use_case import IManagerLevelingUseCase
from app.domain.game.use_cases.i_viewers_websocket_manager import IViewersWebSocketManager
from app.repositories.auth.auth_repository import AuthRepository


class GameUseCase(IGameUseCase):
    websocket_manager: IGameWebSocketManager
    viewers_websocket_manager: IViewersWebSocketManager
    leveling_manager: IManagerLevelingUseCase
    repo: AuthRepository

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
            return 0

    def _update_player_scores(self, game: Game) -> None:  # noqa
        """Update the current players scores"""
        game.p1.board.get_score()
        game.p2.board.get_score()

    def _get_user(self, user_id: str) -> User:
        """Create an instance of the user by the user id"""
        user = self.repo.get_user_by_id(user_id)
        user.user_level = self.repo.get_user_level(user.user_id)
        user.bank_account = self.repo.get_user_bank_account(user.user_id)
        return user

    def _update_user_level_rank_and_bank_account(self, exp_points, winner_player):
        """Update Winner level, rank and bank account.

        This method is used after the game finished or when the usr disconnect.
        Note: Only update the bank account if the user level up. We have a fix amount by the moment, but later
        could change this for a dynamic formula.
        """
        old_user: User = copy.deepcopy(winner_player.user)
        user = self.leveling_manager.update_user_level(winner_player.user, exp_points)
        # Update user bank account if level up:
        if old_user.user_level.level != user.user_level.level:
            win_amount = 100
            new_amount = user.bank_account.amount + win_amount
            self.repo.update_user_bank_account_amount(user.user_id, new_amount)
        self.repo.update_user_level(user.user_level)

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
        game = self.websocket_manager.active_games.get(game_id)
        if not game:
            player = self._create_new_player(self._get_user(user_id))
            game = self._create_new_game(game_id, player)
            await self.websocket_manager.connect(game_id=game_id, new_game=game, websocket=websocket)
        else:
            player = self._create_new_player(self._get_user(user_id))
            game.p2 = player
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

    def get_valid_game_id(self, user_id: str, game_id: str) -> str:
        game = self.websocket_manager.active_games.get(game_id)
        if game_id == 'new_game':
            return str(uuid.uuid4())
        if game and game.p1.user.user_id != user_id:
            return game_id
        else:
            raise WebSocketException(code=status.WS_1014_BAD_GATEWAY, reason='You are already in the match.')

    async def get_winner_after_player_disconnect(self, disconnected_player: Player, game: Game,
                                                 websocket: WebSocket) -> None:
        # There doesn't need to be a winner. Because after the winner player disconnect from the game will trigger this event.
        # Also is necessary to have a player 2 in the match. Without him this means the match never started.
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

    def save_game_history(self, game: Game) -> None:
        """Save the game match result"""
        play_history = PlayHistory.from_game(game)
        self.repo.save_game_history(play_history)
        self.repo.save_user_play_history(game.p1.user, play_history)
        self.repo.save_user_play_history(game.p2.user, play_history)

    def save_single_game_history(self, game: Game, column_index: int) -> None:
        """Save single game history player column selection"""
        single_game_history = SinglePlayHistory.from_game(game, column_index)
        self.repo.save_single_play_history(single_game_history)

    async def execute(self, game: Game, **kwargs):
        match game.state:
            case GameState.CREATE_NEW_GAME:
                game.state = GameState.WAITING_OPPONENT
                extras = {}
                message = 'player_1_connected'
                await self.websocket_manager.broadcast(game_id=game.game_id, message=message, extras=extras)
                await self.viewers_websocket_manager.broadcast(game=game, message=message, extras=extras)

            case GameState.WAITING_OPPONENT:
                started_player = self._get_starter_player(game)
                game.current_player = started_player
                game.state = GameState.ROLL_DICE
                extras = {}
                message = 'player_2_connected'
                await self.websocket_manager.broadcast(game_id=game.game_id, message=message, extras=extras)
                await self.viewers_websocket_manager.broadcast(game=game, message=message, extras=extras)

            case GameState.ROLL_DICE:
                game.current_player.die.roll()
                game.state = GameState.SELECT_COLUMN
                extras = {}
                message = 'roll_dice'
                await self.websocket_manager.broadcast(game_id=game.game_id, message=message, extras=extras)
                await self.viewers_websocket_manager.broadcast(game=game, message=message, extras=extras)

            case GameState.SELECT_COLUMN:
                request: GamePlayerRequest = kwargs['selected_column']
                column_index = self._select_column(request)
                column = game.current_player.board.columns.get(column_index)
                if column_index and not column.is_full():
                    # This save the result move from the user. This table helps to the machine learning model.
                    # Only save the Human inputs to train the model.
                    if game.current_player.rol == PlayerRol.HUMAN:
                        self.save_single_game_history(game, column_index)
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
                    await self.viewers_websocket_manager.broadcast(game=game, message=message, extras=extras)
                    await self.execute(game)

            case GameState.DESTROY_OPPONENT_TARGET_COLUMN:
                column_opponent_player: Column = kwargs['column_opponent_player']
                die_val: int = kwargs['die_val']
                removed_indices = column_opponent_player.remove(die_val)
                game.state = GameState.UPDATE_PLAYERS_POINTS
                extras = {'removed_indices': removed_indices}
                message = 'destroy_opponent_target_column'
                await self.websocket_manager.broadcast(game_id=game.game_id, message=message, extras=extras)
                await self.viewers_websocket_manager.broadcast(game=game, message=message, extras=extras)
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
                await self.viewers_websocket_manager.broadcast(game=game, message=message, extras=extras)

            case GameState.CHANGE_CURRENT_PLAYER:
                game.current_player = game.get_opponent_player()
                game.state = GameState.ROLL_DICE
                extras = {}
                message = 'change_current_player'
                await self.websocket_manager.broadcast(game_id=game.game_id, message=message, extras=extras)
                await self.viewers_websocket_manager.broadcast(game=game, message=message, extras=extras)

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
                await self.viewers_websocket_manager.broadcast(game=game, message=message, extras=extras)
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
