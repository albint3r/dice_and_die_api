from abc import ABC, abstractmethod

from pydantic import BaseModel
from starlette.websockets import WebSocket

from app.domain.auth.entities.user import User
from app.domain.core.ref_types import TGamePlayer
from app.domain.game.entities.board import Board
from app.domain.game.entities.game import Game
from app.domain.game.entities.player import Player
from app.domain.game.schemas.request import GamePlayerRequest


class IGamesModeRunner(BaseModel, ABC):
    """
    Interface for running game modes.

    Attributes:
        Config (class): Configuration options for Pydantic BaseModel.

    Methods:
        play: Run the game.
        verbose: Print the Game for debugging.
        get_valid_game_id: Create, update or maintain the game id to handle where redirect the user.
        create_or_join: Create a new room or joint the user to the room.
        get_user_event_request: Get the player message event from the client.
        get_user: Create an instance of the user by the user id.
        create_new_player: Create a new personalized player.
        create_board: Create Player Board.
        create_new_game: Create a new personalized Game.
        get_starter_player: Select randomly which player would start the game.
        select_column: Player select target index column.
        update_player_scores: Update the current players scores.
        update_user_level_rank_and_bank_account: Update Winner level, rank and bank account.
        update_game_mode_user_level_rank_and_bank_account: Update Winner level, rank and bank account in the Game Mode.
        save_single_game_history: Save single game history player column selection.
        save_game_history: Save the game match result.
        get_winner_after_player_disconnect: Get the winner after a user disconnect before the game ends.
        get_overall_games_winner: This is the final result of the players after playing all the games.
        end_game: End the game Mode.
    """

    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    async def play(self, game: Game, player: Player | None = None,
                   game_events: GamePlayerRequest | None = None, **kwargs) -> None:
        """Run the game"""

    @abstractmethod
    def verbose(self, game: Game) -> None:
        """Print the Game for debugging"""

    @abstractmethod
    def get_valid_game_id(self, user_id: str, game_id: str) -> str:
        """Create, update or maintain the game id to handle where redirect the user."""

    @abstractmethod
    async def create_or_join(self, game_id: str, user_id: str, websocket: WebSocket) -> TGamePlayer:
        """Create a new room or joint the user to the room."""

    @abstractmethod
    async def get_user_event_request(self, websocket: WebSocket) -> GamePlayerRequest:  # noqa
        """Get the player message event from the client"""

    @abstractmethod
    def get_user(self, user_id: str) -> User:
        """Create an instance of the user by the user id"""

    @abstractmethod
    def create_new_player(self, user: User) -> Player:
        """Crete a new personalize player"""

    @abstractmethod
    def create_board(self, max_length: int = 3) -> Board:  # noqa
        """Create Player Board"""

    @abstractmethod
    def create_new_game(self, game_id: str, player: Player) -> Game:
        """Create a new personalize Game"""

    @abstractmethod
    def get_starter_player(self, game: Game) -> Player:  # noqa
        """Select randomly witch player would start the game."""

    @abstractmethod
    def select_column(self, request: GamePlayerRequest) -> int:
        """Player select target index column"""

    @abstractmethod
    def update_player_scores(self, game: Game) -> None:  # noqa
        """Update the current players scores"""

    @abstractmethod
    def update_user_level_rank_and_bank_account(self, exp_points, winner_player):
        """Update Winner level, rank and bank account."""

    @abstractmethod
    def update_game_mode_user_level_rank_and_bank_account(self, exp_points, winner_player):
        """Update Winner level, rank and bank account in the Game Mode"""

    @abstractmethod
    def save_single_game_history(self, game: Game, column_index: int) -> None:
        """Save single game history player column selection"""

    @abstractmethod
    def save_game_history(self, game: Game) -> None:
        """Save the game match result"""

    @abstractmethod
    async def get_winner_after_player_disconnect(self, disconnected_player: Player, game: Game,
                                                 websocket: WebSocket) -> None:
        """Get the winner after a user disconnect before the game ends."""

    @abstractmethod
    async def get_overall_games_winner(self, game: Game, player: Player) -> None:
        """This is the final result of the players after playing all the games."""

    @abstractmethod
    async def end_game(self, game_id: str, websocket: WebSocket) -> None:
        """End the game Mode"""
