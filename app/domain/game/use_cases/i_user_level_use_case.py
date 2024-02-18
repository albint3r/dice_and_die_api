from abc import ABC, abstractmethod

from pydantic import BaseModel

from app.domain.game.use_cases.i_leveling_use_case import ILevelUseCase, IRankUseCase
from src.domain.auth.user import User
from src.domain.core.i_game_manager import IGameManager
from src.domain.game.game import Game


class IManagerLevelingUseCase(BaseModel, ABC):

    @abstractmethod
    def get_winner_earned_exp_points(self, game: Game) -> int:
        """Get how many point the winner get."""

    @abstractmethod
    def update_user_level(self, user: User, exp_points: int,
                          leve_manager: ILevelUseCase,
                          rank_manager: IRankUseCase) -> User:
        """Update User Level after win.
        In this facade the user level will be updated on:
        - Xp points
        - Level
        - Rank

        If any of these conditions apply it will the user entity and returned.
        """
