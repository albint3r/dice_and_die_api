from pydantic import BaseModel
from abc import ABC, abstractmethod

from src.domain.game.game import Game
from src.domain.game.player import Player


class IGameFacade(ABC, BaseModel):

    @abstractmethod
    def new_game(self) -> Game:
        """Run the game"""

    @abstractmethod
    def select_player_start(self, game: Game) -> Player:
        """Select witch player start the game"""

    @abstractmethod
    def select_column(self, **kwargs) -> int:
        """Add player to column"""
