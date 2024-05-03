import copy
import os
import uuid
from random import choice

import joblib
from icecream import ic
from sklearn.ensemble import RandomForestClassifier
from starlette.websockets import WebSocket

from app.domain.analytics.entities.single_play_history import SinglePlayHistory
from app.domain.core.ref_types import TGamePlayer
from app.domain.game.entities.column import Column
from app.domain.game.entities.game import Game
from app.domain.game.entities.player import Player
from app.domain.game.entities.player_rol import PlayerRol
from app.domain.game.enums.game_state import GameState
from app.domain.game.errors.errors import InvalidAIPathModel
from app.infrastructure.game.game_use_case import GameUseCase


class PVEGameUseCase(GameUseCase):

    def _get_starter_player(self, game: Game) -> Player:  # noqa
        """Select randomly witch player would start the game."""
        return game.p1

    def _create_new_game(self, game_id: str, player: Player, player_ai: Player) -> Game:  # noqa
        """Create a new Game."""
        return Game(game_id=game_id, p1=player, p2=player_ai, state=GameState.WAITING_OPPONENT)

    async def create_or_join(self, game_id: str, user_id: str, websocket: WebSocket) -> TGamePlayer:
        """Create a room for the player and an AI."""
        player = self._create_new_player(self._get_user(user_id))
        player_ai = self._create_new_player(self._get_user('I007'))
        player_ai.rol = PlayerRol.AI
        game = self._create_new_game(game_id, player, player_ai)
        await self.websocket_manager.connect(game_id=game_id, new_game=game, websocket=websocket)
        return game, player

    async def get_winner_after_player_disconnect(self, disconnected_player: Player, game: Game,
                                                 websocket: WebSocket) -> None:
        return NotImplemented('[get_winner_after_player_disconnect] IS NOT IMPLEMENTED')

    def get_valid_game_id(self, _: str, __: str) -> str:
        return str(uuid.uuid4())

    def _simulate_remove_values_from_column(self, column: Column, die_value: int) -> Column:
        old_column: Column = copy.deepcopy(column)
        if old_column.is_empty():
            return old_column

        for value in old_column.values:
            if value == die_value:
                old_column.values.remove(value)
        old_column.get_score()
        return old_column

    def _simulate_add_values_from_column(self, column: Column, die_value: int) -> Column:
        old_column: Column = copy.deepcopy(column)
        if not old_column.is_full():
            old_column.add(die_value)
        old_column.get_score()
        return old_column

    def _get_ai_selected_column_by_zero_sum(self, game: Game) -> str:
        """This use the zero-sum strategy to select the column.

        This strategy consist in select the column that give the AI they must number of points.
        """
        die_val = game.p2.die.current_number
        ic(die_val)
        max_points = float('-inf')
        best_index = None
        # Check each column scenario
        ic(game.p1.board.columns)
        ic(game.p2.board.columns)
        for i in range(1, 4):
            p1_column = game.p1.board.columns.get(i)
            p2_column = game.p2.board.columns.get(i)
            # Now simulate the column score. We need to create a copy of the column
            if not p2_column.is_full():
                p2_simulate_column = self._simulate_add_values_from_column(p2_column, die_val)
                p1_simulate_column = self._simulate_remove_values_from_column(p1_column, die_val)
                ic(p1_simulate_column)
                ic(p2_simulate_column)
                old_result = ic(p2_column.score - p1_column.score)
                simulate_result = ic(p2_simulate_column.score - p1_simulate_column.score)
                result = ic(simulate_result - old_result)
                ic(max_points)
                if result >= max_points:
                    max_points = result
                    best_index = i
        ic(best_index)
        return str(best_index)

    def _get_ai_selected_column_by_machinelearning(self, game: Game) -> str:
        model_file = 'best_estimator.pkl'
        if not os.path.exists(model_file):
            raise InvalidAIPathModel('Not AI model path.')

        best_rf_model_loaded: RandomForestClassifier = joblib.load(model_file)
        single_play_history = SinglePlayHistory.from_game(game, 0)
        X = single_play_history.to_array()
        y_pred = best_rf_model_loaded.predict(X)
        return str(y_pred[0])

    def get_ai_selected_column(self, game: Game) -> str:  # noqa
        """Return the index integer of the column to select by the AI"""
        ai_bag = choice([self._get_ai_selected_column_by_zero_sum, self._get_ai_selected_column_by_machinelearning,
                         self._get_ai_selected_column_by_machinelearning])
        index_column = self._get_ai_selected_column_by_zero_sum(game)
        columns = game.p2.board.columns
        available_columns = [str(i) for i, col in columns.items() if not col.is_full()]
        if index_column in available_columns:
            return index_column
        return choice(available_columns)
