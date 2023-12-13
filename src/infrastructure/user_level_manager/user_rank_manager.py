from pydantic import BaseModel, validate_call

from src.domain.auth.user_level import UserLevel


class IUserRankManager(BaseModel):

    @validate_call()
    def next_rank(self, user_level: UserLevel):
        """Get How Many Point Need for the next level"""

    @validate_call()
    def ready_to_rank_up(self, user_level: UserLevel):
        """Check if the user have equal or more point to upgrade to the next level"""
