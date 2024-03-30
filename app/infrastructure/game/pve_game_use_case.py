import uuid
from random import choice

import joblib
from icecream import ic
from sklearn.ensemble import RandomForestClassifier
from starlette.websockets import WebSocket

from app.domain.analytics.entities.single_play_history import SinglePlayHistory
from app.domain.core.ref_types import TGamePlayer
from app.domain.game.entities.game import Game
from app.domain.game.entities.player import Player
from app.domain.game.entities.player_rol import PlayerRol
from app.domain.game.enums.game_state import GameState
from app.domain.game.errors.errors import InvalidAIPathModel
from app.infrastructure.game.game_use_case import GameUseCase
import os


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

    def get_ai_selected_column(self, game: Game) -> str:  # noqa
        """Return the index integer of the column to select by the AI"""

        model_file = 'best_estimator.pkl'
        ic(model_file)
        if not os.path.exists(model_file):
            raise InvalidAIPathModel('Not AI model path.')

        best_rf_model_loaded: RandomForestClassifier = joblib.load(model_file)
        single_play_history = SinglePlayHistory.from_game(game, 0)
        X = single_play_history.to_array()
        y_pred = best_rf_model_loaded.predict(X)
        index_column = str(y_pred[0])
        columns = game.p2.board.columns
        available_columns = [str(i) for i, col in columns.items() if not col.is_full()]
        if index_column in available_columns:
            ic('It was used the ML model')
            return index_column
        return choice(available_columns)
