from typing import Callable

from pydantic import BaseModel, validate_call

from src.domain.auth.user_level import UserLevel


def next_level_basic_formula(user_level: UserLevel) -> int:
    level = user_level.level
    exponent1 = 0.1
    exponent2 = 0.8
    base_exp = 50
    return int(exponent1 * (level ** 3) + exponent2 * (level ** 2) + base_exp * level)


def next_level_advance_formula(user_level: UserLevel) -> int:
    exponent = 1.5
    base_exp = 100
    return int(base_exp * (user_level.level ** exponent))


class UserLevelManager(BaseModel):

    @validate_call()
    def next_level(self, user_level: UserLevel, *, formula: Callable[[UserLevel], int]) -> int:
        """Get How Many Point Need for the next level"""
        return formula(user_level)

    @validate_call()
    def ready_to_level_up(self, user_level: UserLevel, *,
                          formula: Callable[[UserLevel], int] = next_level_basic_formula) -> bool:
        """Check if the user have equal or more point to upgrade to the next level"""
        points_to_next_lvl = formula(user_level)
        return user_level.current_points >= points_to_next_lvl

    @validate_call()
    def add_exp_points(self, user_level: UserLevel, exp_points: int) -> int:
        """Add experience point to the user level"""
        return user_level.current_points + exp_points
