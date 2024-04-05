import copy
from json import JSONDecodeError
from random import choice

from icecream import ic
from pydantic import ValidationError
from starlette.websockets import WebSocket

from app.domain.analytics.entities.single_play_history import SinglePlayHistory
from app.domain.auth.entities.user import User
from app.domain.core.ref_types import TGamePlayer
from app.domain.game.entities.board import Board
from app.domain.game.entities.column import Column
from app.domain.game.entities.die import Die
from app.domain.game.entities.game import Game, TWinner
from app.domain.game.entities.game_config import GameConfig
from app.domain.game.entities.play_history import PlayHistory
from app.domain.game.entities.player import Player
from app.domain.game.entities.player_rol import PlayerRol
from app.domain.game.enums.game_event import GameEvent
from app.domain.game.enums.game_mode import GameMode, RematchMode
from app.domain.game.enums.game_state import GameState
from app.domain.game.errors.errors import SinglePlaHistoryDontMatchColumnsLength, PlaHistoryDontMatchColumnsLength
from app.domain.game.schemas.request import GamePlayerRequest
from app.domain.game.use_cases.i_game_websocket_manager import IGameWebSocketManager
from app.domain.game.use_cases.i_games_mode_runner import IGamesModeRunner
from app.domain.game.use_cases.i_user_level_use_case import IManagerLevelingUseCase
from app.domain.game.use_cases.i_viewers_websocket_manager import IViewersWebSocketManager
from app.repositories.auth.auth_repository import AuthRepository


class AdventureGameModeRunner(IGamesModeRunner):
    repo: AuthRepository
    ws_game: IGameWebSocketManager
    ws_viewers: IViewersWebSocketManager
    leveling_manager: IManagerLevelingUseCase

    async def play(self, game: Game, player: Player | None = None,
                   game_events: GamePlayerRequest | None = None, **kwargs) -> None:
        match game.state:
            case GameState.CREATE_NEW_GAME:
                await self._create_new_game(game)

            case GameState.WAITING_OPPONENT:
                await self._waiting_opponent(game)

            case GameState.ROLL_DICE:
                await self._roll_dice(game, game_events)

            case GameState.SELECT_COLUMN:
                await self._select_column(game, game_events, player)

            case GameState.ADD_DICE_TO_COLUMN:
                await self._add_dice_to_column(game, kwargs)

            case GameState.DESTROY_OPPONENT_TARGET_COLUMN:
                await self._destroy_opponent_target_column(game, kwargs)

            case GameState.UPDATE_PLAYERS_POINTS:
                await self._update_players_points(game)

            case GameState.CHANGE_CURRENT_PLAYER:
                await self._change_current_player(game)

            case GameState.FINISH_GAME:
                await self._finish_game(game)

            case GameState.REMATCH:
                await self._rematch(game, game_events, player)

            case GameState.DISCONNECT_PLAYER:
                await self._disconnect_player(game)

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
        await self.play(game)
        return game, player

    async def get_user_event_request(self, websocket: WebSocket) -> GamePlayerRequest:  # noqa
        """Get the player message event from the client"""
        try:
            json_str = await websocket.receive_json()
            return GamePlayerRequest(**json_str)
        except ValidationError:
            return GamePlayerRequest(event=GameEvent.INVALID_INPUT_EVENT)
        except JSONDecodeError:
            return GamePlayerRequest(event=GameEvent.INVALID_INPUT_EVENT)

    def create_new_game(self, game_id: str, player: Player) -> Game:
        config = GameConfig(game_mode=GameMode.CLASSIC,
                            rematch_mode=RematchMode.best_total_games_score,
                            col_length=1,
                            total_columns=1,
                            total_games=3)
        return Game(game_id=game_id, p1=player, state=GameState.CREATE_NEW_GAME, config=config)

    def create_new_player(self, user: User) -> Player:
        return Player(user=user,
                      board=self.create_board(),
                      die=Die()
                      )

    def get_user(self, user_id: str) -> User:
        user = self.repo.get_user_by_id(user_id)
        user.user_level = self.repo.get_user_level(user.user_id)
        user.bank_account = self.repo.get_user_bank_account(user.user_id)
        return user

    def select_column(self, request: GamePlayerRequest) -> int:
        try:
            return int(request.event.value)
        except ValueError:
            return 0

    def update_player_scores(self, game: Game) -> None:  # noqa
        """Update the current players scores"""
        game.p1.board.get_score()
        game.p2.board.get_score()

    async def get_winner_after_player_disconnect(self, disconnected_player: Player, game: Game,
                                                 websocket: WebSocket) -> None:
        """Get the winner after a user disconnect before the game ends."""
        # There doesn't need to be a winner. Because after the winner player disconnect from the game will trigger this event.
        # Also is necessary to have a player 2 in the match. Without him this means the match never started.
        if not game.winner_player and game.p2:
            await self.ws_game.disconnect(game_id=game.game_id, websocket=websocket)
            connection = self.ws_game.get_remained_player_websocket(game.game_id)
            if connection:
                game.winner_player = (game.p1, None) if disconnected_player is game.p2 else (game.p2, None)
                game.state = GameState.DISCONNECT_PLAYER
                await self.play(game)
        # If is not opponent disconnect safe.
        else:
            await self.ws_game.disconnect(game_id=game.game_id, websocket=websocket)

    # Todo: add to abs methods
    # Create class to handle the confing last result exp and rewards
    async def get_overall_games_winner(self, game: Game) -> TWinner:
        """This is the final result of the players after playing all the games."""
        p1_score = game.config.wins_counter.get(game.p1.user.user_id, 0)
        p2_score = game.config.wins_counter.get(game.p2.user.user_id, 0)
        if p1_score > p2_score:
            winner_player = (game.p1, None)
        elif p2_score > p1_score:
            winner_player = (game.p2, None)
        else:
            winner_player = (game.p1, game.p2)

        return winner_player

    def verbose(self, game: Game) -> None:
        ic('/' * 100)
        ic(f'Current player: {game.current_player.user.name} | Die:{game.current_player.die.current_number}')
        ic(f'GameState: {game.state}')
        ic('/' * 100)
        ic(f'Player 2:{game.p2.user.name}')
        ic(game.p2.board.columns.get(1), game.p2.board.columns.get(2), game.p2.board.columns.get(3),
           game.p2.board.columns.get(4))
        ic('.' * 100)
        ic(f'Player 1:{game.p1.user.name}')
        ic(game.p1.board.columns.get(1), game.p1.board.columns.get(2), game.p1.board.columns.get(3),
           game.p1.board.columns.get(4))
        ic('*-' * 100)

    def create_board(self, max_length: int = 1) -> Board:  # noqa
        return Board(columns={i: Column(max_length=max_length) for i in range(1, max_length + 1)})

    def get_starter_player(self, game: Game) -> Player:  # noqa
        """Select randomly witch player would start the game."""
        return choice([game.p1, game.p2])

    def update_user_level_rank_and_bank_account(self, exp_points, winner_player):
        """Update Winner level, rank and bank account.

        This method is used after the game finished or when the usr disconnect.
        Note: Only update the bank account if the user level up. We have a fix amount by the moment, but later
        could change this for a dynamic formula.
        """
        old_user: User = copy.deepcopy(winner_player.user)
        user = self.leveling_manager.update_user_level(winner_player.user, exp_points)
        # Update user bank account if level up:
        if old_user.user_level.level != user.user_level.level:
            self.repo.update_user_bank_account_amount(user.user_id, 100.0)
        self.repo.update_user_level(user.user_level)

    def save_game_history(self, game: Game) -> None:
        """Save the game match result"""
        try:
            play_history = PlayHistory.from_game(game)
            self.repo.save_game_history(play_history)
            self.repo.save_user_play_history(game.p1.user, play_history)
            self.repo.save_user_play_history(game.p2.user, play_history)
        except PlaHistoryDontMatchColumnsLength:
            ic('Game wont be saved')

    def save_single_game_history(self, game: Game, column_index: int) -> None:
        """Save single game history player column selection"""
        try:
            single_game_history = SinglePlayHistory.from_game(game, column_index)
            self.repo.save_single_play_history(single_game_history)
        except SinglePlaHistoryDontMatchColumnsLength:
            ic('Game wont be saved')

    async def _disconnect_player(self, game):
        winner_player, _ = game.winner_player
        exp_points = self.leveling_manager.get_winner_earned_exp_after_player_disconnect()
        # Create a copy to compare if the user level up
        self.update_user_level_rank_and_bank_account(exp_points, winner_player)
        extras = {}
        message = 'player_disconnected'
        await self.ws_game.broadcast(game_id=game.game_id, message=message, extras=extras)
        await self.ws_viewers.broadcast(game=game, message=message, extras=extras)

    async def _rematch(self, game, game_events, player):
        if game_events.event == GameEvent.NO:
            game.config.is_game_mode_over = True
        if game_events.event == GameEvent.YES:
            if player == game.p1:
                game.p1.reset_board(game.config.col_length, game.config.total_columns)
                game.config.confirm_player_rematch_game(player)
            else:
                game.p2.reset_board(game.config.col_length, game.config.total_columns)
                game.config.confirm_player_rematch_game(player)
        if game.config.is_rematch:
            game.current_player = None
            game.winner_player = None
            game.current_turn = 0
            started_player = self.get_starter_player(game)
            game.current_player = started_player
            game.state = GameState.ROLL_DICE
            extras = {}
            message = 'roll_dice'
            await self.ws_game.broadcast(game_id=game.game_id, message=message, extras=extras)
            game.config.reset_confirmed_players_rematch_game()

    async def _finish_game(self, game):
        winner_player, tied_player = game.get_winner()
        exp_points = self.leveling_manager.get_winner_earned_exp_points(game)
        if tied_player:
            # Update both players points and ranks
            self.update_user_level_rank_and_bank_account(exp_points, tied_player)
            game.config.update_wins_counter(tied_player)
        self.update_user_level_rank_and_bank_account(exp_points, winner_player)
        game.config.update_wins_counter(winner_player)
        if not game.config.are_all_games_played():
            game.state = GameState.REMATCH
        extras = {}
        message = 'finish_game'
        await self.ws_game.broadcast(game_id=game.game_id, message=message, extras=extras)
        self.save_game_history(game)

    async def _change_current_player(self, game):
        game.current_player = game.get_opponent_player()
        game.state = GameState.ROLL_DICE
        extras = {}
        message = 'change_current_player'
        await self.ws_game.broadcast(game_id=game.game_id, message=message, extras=extras)

    async def _update_players_points(self, game):
        self.update_player_scores(game)
        if game.is_finished:
            game.state = GameState.FINISH_GAME
        else:
            game.state = GameState.CHANGE_CURRENT_PLAYER
        extras = {}
        message = 'update_players_points'
        await self.ws_game.broadcast(game_id=game.game_id, message=message, extras=extras)
        await self.play(game)

    async def _destroy_opponent_target_column(self, game, kwargs):
        column_opponent_player: Column = kwargs['column_opponent_player']
        die_val: int = kwargs['die_val']
        removed_indices = column_opponent_player.remove(die_val)
        game.state = GameState.UPDATE_PLAYERS_POINTS
        extras = {'removed_indices': removed_indices}
        message = 'destroy_opponent_target_column'
        await self.ws_game.broadcast(game_id=game.game_id, message=message, extras=extras)
        await self.play(game)

    async def _add_dice_to_column(self, game, kwargs):
        column_index: int = kwargs['column_index']
        column = game.current_player.board.columns.get(column_index)
        die_val = game.current_player.die.current_number
        column.add(die_val)
        opponent_player = game.get_opponent_player()
        column_opponent_player = opponent_player.board.columns.get(column_index)
        if column_opponent_player.can_remove_values(die_val):
            game.state = GameState.DESTROY_OPPONENT_TARGET_COLUMN
            await self.play(game, column_opponent_player=column_opponent_player, die_val=die_val)
        else:
            game.state = GameState.UPDATE_PLAYERS_POINTS
            extras = {}
            message = 'add_dice'
            await self.ws_game.broadcast(game_id=game.game_id, message=message, extras=extras)
            await self.play(game)

    async def _select_column(self, game, game_events, player):
        column_index = self.select_column(game_events)
        column = game.current_player.board.columns.get(column_index)
        if column and not column.is_full():
            # This save the result move from the user. This table helps to the machine learning model.
            # Only save the Human inputs to train the model.
            if game.current_player.rol == PlayerRol.HUMAN:
                self.save_single_game_history(game, column_index)
            game.state = GameState.ADD_DICE_TO_COLUMN
            await self.play(game, player, column_index=column_index)

    async def _roll_dice(self, game, game_events):
        if game_events.event == GameEvent.ROLL:
            game.current_player.die.roll()
            game.state = GameState.SELECT_COLUMN
            extras = {}
            message = 'roll_dice'
            await self.ws_game.broadcast(game_id=game.game_id, message=message, extras=extras)

    async def _waiting_opponent(self, game):
        started_player = self.get_starter_player(game)
        game.current_player = started_player
        game.state = GameState.ROLL_DICE
        extras = {}
        message = 'player_2_connected'
        await self.ws_game.broadcast(game_id=game.game_id, message=message, extras=extras)

    async def _create_new_game(self, game):
        game.state = GameState.WAITING_OPPONENT
        extras = {}
        message = 'player_1_connected'
        await self.ws_game.broadcast(game_id=game.game_id, message=message, extras=extras)
