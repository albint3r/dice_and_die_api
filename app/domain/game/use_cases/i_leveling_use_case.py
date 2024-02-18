from typing import Callable

from pydantic import BaseModel
from abc import ABC, abstractmethod

from app.domain.auth.entities.user_level import UserLevel
from app.domain.auth.enums.rank import Rank


class ILeveling(BaseModel, ABC):

    @abstractmethod
    def next_stage(self, *args, **kwargs) -> int:
        """Get the points needed to reach the next stage (level or rank)"""
        pass

    @abstractmethod
    def ready_to_progress(self, *args, **kwargs) -> bool:
        """Check if the user has enough points to progress to the next stage"""
        pass

    @abstractmethod
    def progress(self, *args, **kwargs):
        """Progress the user to the next stage"""


class IRankUseCase(ILeveling, ABC):
    @abstractmethod
    def next_stage(self, rank: Rank) -> int:
        """Get the Level the user need to rank up.
        Example: The user is STONE, so he needs to be level 5 to pass to IRON.
        """

    @abstractmethod
    def ready_to_progress(self, user_level: UserLevel) -> bool:
        """Check if the user have equal or more point to upgrade to the next Rank"""

    @abstractmethod
    def progress(self, user_level: UserLevel):
        """Add experience level """


class ILevelUseCase(ILeveling, ABC):

    @abstractmethod
    def next_stage(self, user_level: UserLevel, *,
                   formula: Callable[[UserLevel], int]) -> int:
        """Get How Many Point Needs for the next level"""

    @abstractmethod
    def ready_to_progress(self, user_level: UserLevel, *,
                          formula: Callable[[UserLevel], int]) -> bool:
        """Check if the user have equal or more point to upgrade to the next level"""

    @abstractmethod
    def progress(self, user_level: UserLevel,
                 formula: Callable[[UserLevel], int]):
        """Add experience level """

    @abstractmethod
    def add_exp_points(self, user_level: UserLevel, exp_points: int) -> int:
        """Add experience point to the user level"""
