from pydantic import validate_call

from src.db.db import AbstractDB
from src.domain.user.errors import NoUserInRanking
from src.domain.user.user_rank import UserRank


class UserRepository(AbstractDB):

    @validate_call()
    def update_user_name_and_last_name(self, user_id: str, name: str, last_name: str) -> None:
        """Update in the db the name and last name of the user id."""
        query = f"UPDATE users SET name='{name}', last_name='{last_name}' WHERE user_id='{user_id}';"
        self.db.execute(query)

    @validate_call()
    def get_users_ranking(self) -> list[UserRank]:
        """Update in the db the name and last name of the user id."""
        query = "SELECT u.name, u.last_name, us.level, us.exp_points, us.rank_id " \
                "FROM users AS u " \
                "JOIN users_levels AS us ON us.user_id= u.user_id " \
                "ORDER BY us.level DESC, us.exp_points DESC;"
        result = self.db.query(query, fetch_all=True)
        if result:
            return [UserRank(**user) for user in result]
        raise NoUserInRanking('There is not user in the ranking leader. Crear user first')
