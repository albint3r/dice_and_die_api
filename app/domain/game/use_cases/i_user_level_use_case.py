from abc import ABC, abstractmethod

from pydantic import BaseModel

from src.domain.auth.user import User
from src.domain.core.i_game_manager import IGameManager
from src.domain.game.game import Game


class IManagerLevelingUseCase(BaseModel, ABC):

    @abstractmethod
    def get_winner_earned_exp_points(self, game: Game) -> int:
        """Get how many point the winner get."""

    @abstractmethod
    def update_user_level(self, user: User, exp_points: int,
                          leve_manager: IGameManager,
                          rank_manager: IGameManager) -> User:
        """Update the user experience points"""
