from typing import Callable

from app.domain.auth.entities.user_level import UserLevel
from app.domain.game.use_cases.i_leveling_use_case import ILevelUseCase


class LevelUserCase(ILevelUseCase):
    def next_stage(self, user_level: UserLevel, *, formula: Callable[[UserLevel], int]) -> int:
        return formula(user_level)

    def ready_to_progress(self, user_level: UserLevel, *, formula: Callable[[UserLevel], int]) -> bool:
        points_to_next_lvl = self.next_level(user_level, formula=formula)
        return user_level.exp_points >= points_to_next_lvl

    def progress(self, user_level: UserLevel, formula: Callable[[UserLevel], int]):
        user_level.level += 1
        # Update how many points need for the next level?
        user_level.next_level_points = self.next_level(user_level, formula=formula)
        return user_level

    def add_exp_points(self, user_level: UserLevel, exp_points: int) -> int:
        return user_level.exp_points + exp_points
