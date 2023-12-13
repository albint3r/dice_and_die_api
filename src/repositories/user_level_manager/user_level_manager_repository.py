from icecream import ic

from src.db.db import AbstractDB
from pydantic import validate_call

from src.domain.auth.user_level import UserLevel


class UserLeveRepository(AbstractDB):

    @validate_call()
    def update_user_level(self, user_level: UserLevel) -> None:
        """Update the level and experience points of the user level"""
        query = f"UPDATE users_levels SET level = {user_level.level}, exp_points = {user_level.exp_points}, " \
                f"rank_id = {user_level.rank_id} " \
                f"WHERE user_id = '{user_level.user_id}';"
        ic(query)
        self.db.execute(query)
