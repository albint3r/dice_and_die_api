from icecream import ic

from src.db.db import AbstractDB
from pydantic import validate_call

from src.domain.auth.user import User


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
