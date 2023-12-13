from typing import Callable

from pydantic import validate_call

from src.domain.auth.user_level import UserLevel
from src.domain.core.i_game_manager import IGameManager
from src.infrastructure.user_level_manager.utils import next_level_basic_formula


class _LevelManager(IGameManager):

    @validate_call()
    def next_level(self, user_level: UserLevel, *, formula: Callable[[UserLevel], int]) -> int:
        """Get How Many Point Needs for the next level"""
        return formula(user_level)

    @validate_call()
    def ready_to_level_up(self, user_level: UserLevel, *,
                          formula: Callable[[UserLevel], int] = next_level_basic_formula) -> bool:
        """Check if the user have equal or more point to upgrade to the next level"""
        points_to_next_lvl = self.next_level(user_level, formula=formula)
        return user_level.exp_points >= points_to_next_lvl

    @validate_call()
    def add_exp_points(self, user_level: UserLevel, exp_points: int) -> int:
        """Add experience point to the user level"""
        return user_level.exp_points + exp_points

    @validate_call()
    def add_level_up(self, user_level: UserLevel,
                     formula: Callable[[UserLevel], int] = next_level_basic_formula) -> UserLevel:
        """Add experience level """
        # Update current level
        user_level.level += 1
        # Update how many points need for the next level?
        user_level.next_level_points = self.next_level(user_level, formula=formula)
        return user_level


level_manager = _LevelManager()
