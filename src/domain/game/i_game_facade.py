from pydantic import BaseModel
from abc import ABC, abstractmethod

from starlette.websockets import WebSocket

from src.domain.game.game import Game
from src.domain.game.player import Player


class IGameFacade(ABC, BaseModel):

    @abstractmethod
    def new_game(self, game_id: str) -> Game:
        """Run the game"""

    @abstractmethod
    def select_player_start(self, game: Game) -> Player:
        """Select witch player start the game"""

    @abstractmethod
    def select_column(self, **kwargs) -> int:
        """Add player to column"""


class IGameWebSocketFacade(IGameFacade, ABC):

    @abstractmethod
    def is_full_room(self, game_id: str) -> bool:
        """Validate if the game is full. Have 2 players."""

    @abstractmethod
    def exist_game(self, game_id: str) -> bool:
        """Validate if the Game/Room already exist"""

    @abstractmethod
    def get_game(self, game_id: str) -> Game:
        """Get existed game"""

    @abstractmethod
    def join_waiting_room(self, game_id: str, player: Player) -> None:
        """Join Player to the waiting room."""

    @abstractmethod
    def get_winner_after_player_disconnect(self, player: Player, game: Game, game_id: str, websocket: WebSocket):
        """Get the remaining player in the room to selected as the winner. In this proces
        We take the opportunity to remove the disconnected player and update the board"""
