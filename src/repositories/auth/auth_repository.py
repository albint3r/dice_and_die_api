from src.db.db import AbstractDB
from pydantic import validate_call

from src.domain.auth.bank_account import BankAccount
from src.domain.auth.errors import UserLevelNotExist
from src.domain.auth.user import User
from src.domain.auth.user_level import UserLevel


class AuthRepository(AbstractDB):
    """Authenticated repository"""

    @validate_call()
    def get_user(self, email) -> User | None:
        """Get the user from the database"""
        query = f'SELECT * FROM users WHERE email="{email}";'
        result = self.db.query(query)
        if result:
            return User(**result)

    @validate_call()
    def create_user(self, email: str, password: str | bytes) -> None:
        """Get the user from the database"""
        query = f"INSERT INTO users (email, password) VALUES ('{email}', '{password}')"
        self.db.execute(query)

    @validate_call()
    def get_user_level(self, user_id: str) -> UserLevel:
        """Get the User Level by the user id."""
        query = f"SELECT * FROM users_levels WHERE user_id='{user_id}';"
        result = self.db.query(query)
        if result:
            return UserLevel(**result)
        raise UserLevelNotExist('User ID no match with the User Level Table Information.')

    @validate_call()
    def create_user_level(self, user_id: str) -> None:
        """Create a new User Level Item"""
        query = f"INSERT INTO users_levels (user_id) VALUES ('{user_id}');"
        self.db.execute(query)

    @validate_call()
    def get_user_bank_account(self, user_id: str) -> BankAccount:
        """Create a new User Bank Account"""
        query = f'SELECT * FROM bank_accounts WHERE user_id="{user_id}";'
        result = self.db.query(query)
        if result:
            return BankAccount(**result)

    @validate_call()
    def create_user_bank_account(self, user_id: str) -> None:
        """Create a new User Bank Account"""
        query = f'INSERT INTO bank_accounts (user_id) VALUES ("{user_id}");'
        self.db.execute(query)
