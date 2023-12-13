from pydantic import BaseModel, validate_call

from src.domain.auth.user_level import UserLevel


class UserLevelManager(BaseModel):
    exponent: float = 1.5
    base_exp: int = 1000

    @validate_call()
    def next_level(self, user_level: UserLevel) -> int:
        """Get How Many Point Need for the next level"""
        return int(self.base_exp * (user_level.level ** self.exponent))

    @validate_call()
    def ready_to_level_up(self, user_level: UserLevel) -> bool:
        """Check if the user have equal or more point to upgrade to the next level"""

    @validate_call()
    def add_exp_points(self, user_level: UserLevel, exp_points: int) -> int:
        """Add experience point to the user level"""
