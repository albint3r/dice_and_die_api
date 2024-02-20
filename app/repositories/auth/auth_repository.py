from pydantic import BaseModel

from app.db.db import _DataBase  # noqa
from app.domain.auth.entities.bank_account import BankAccount
from app.domain.auth.entities.user import User
from app.domain.auth.entities.user_level import UserLevel
from app.domain.auth.entities.user_rank import UserRank
from app.domain.auth.errors.errors import UserLevelNotExist, NoUserInRanking


class AuthRepository(BaseModel):
    """Authenticated repository"""
    db: _DataBase

    def get_user(self, email: str) -> User:
        """Get the user from the database"""
        query = 'SELECT * FROM users WHERE email=%s;'
        result = self.db.query(query, (email,), fetch_all=False)
        if result:
            return User(**result)

    def get_user_by_id(self, user_id: str) -> User | None:
        """Get the user from the database"""
        query = 'SELECT * FROM users WHERE user_id=%s;'
        result = self.db.query(query, (user_id,), fetch_all=False)
        if result:
            return User(**result)

    def create_user(self, email: str, password: str | bytes) -> None:
        """Create a new user"""
        query = "INSERT INTO users (email, password) VALUES (%s, %s);"
        self.db.execute(query, (email, password))

    def delete_user(self, user_id: str) -> None:
        """Delete a user by user_id"""
        query = "DELETE FROM users WHERE user_id=%s;"
        self.db.execute(query, (user_id,))

    def get_user_level(self, user_id: str) -> UserLevel:
        """Get the User Level by the user id."""
        query = "SELECT * FROM users_levels WHERE user_id=%s;"
        result = self.db.query(query, (user_id,), fetch_all=False)
        if result:
            return UserLevel(**result)
        raise UserLevelNotExist('[User] ID no match with the User Level Table Information.')

    def create_user_level(self, user_id: str) -> None:
        """Create a new User Level Item"""
        query = "INSERT INTO users_levels (user_id) VALUES (%s);"
        self.db.execute(query, (user_id,))

    def get_user_bank_account(self, user_id: str) -> BankAccount:
        """Get the bank account of a user"""
        query = "SELECT * FROM bank_accounts WHERE user_id=%s;"
        result = self.db.query(query, (user_id,), fetch_all=False)
        if result:
            return BankAccount(**result)

    def create_user_bank_account(self, user_id: str) -> None:
        """Create a new bank account for a user"""
        query = "INSERT INTO bank_accounts (user_id) VALUES (%s);"
        self.db.execute(query, (user_id,))

    def update_user_name_and_last_name(self, user_id: str, name: str, last_name: str) -> None:
        """Update in the db the name and last name of the user id."""
        query = "UPDATE users SET name=%s, last_name=%s WHERE user_id=%s;"
        self.db.execute(query, (name, last_name, user_id))

    def get_users_ranking(self) -> list[UserRank]:
        """Update in the db the name and last name of the user id."""
        query = "SELECT u.name, u.last_name, us.level, us.exp_points, us.rank_id " \
                "FROM users AS u " \
                "JOIN users_levels AS us ON us.user_id= u.user_id " \
                "ORDER BY us.level DESC, us.exp_points DESC;"
        result = self.db.query(query, (), fetch_all=True)
        if result:
            return [UserRank(**user) for user in result]
        raise NoUserInRanking('There is not user in the ranking leader. Crear user first')

    def update_user_level(self, user_level: UserLevel) -> None:
        """Update the level and experience points of the user level"""
        query = "UPDATE users_levels SET " \
                "level = %s, " \
                "exp_points = %s, " \
                "next_level_points = %s, " \
                "rank_id = %s " \
                "WHERE user_id = %s;"
        values = (user_level.level, user_level.exp_points, user_level.next_level_points, user_level.rank_id,
                  user_level.user_id)
        self.db.execute(query, values)
