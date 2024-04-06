from abc import ABC, abstractmethod

from pydantic import BaseModel

from app.domain.auth.entities.user import User
from app.domain.game.use_cases.i_progress_use_case import ILevelUseCase, IRankUseCase


class IManagerLevelingUseCase(BaseModel, ABC):
    leve_manager: ILevelUseCase
    rank_manager: IRankUseCase

    @abstractmethod
    def get_winner_earned_exp_points(self, *args, **kwargs) -> int:
        """Get how many point the winner get."""

    @abstractmethod
    def get_winner_earned_exp_after_player_disconnect(self) -> int:
        """Get how many point the remaining player get after the other user disconnect"""

    @abstractmethod
    def update_user_level(self, *args, **kwargs) -> User:
        """Update User Level after win.
        In this facade the user level will be updated on:
        - Xp points
        - Level
        - Rank

        If any of these conditions apply it will the user entity and returned.
        """
