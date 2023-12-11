from src.db.db import AbstractDB
from pydantic import validate_call

from src.domain.auth.user import User


class AuthRepository(AbstractDB):
    """Authenticated repository"""

    @validate_call()
    def get_user(self, email: str, password: str) -> User | None:
        """Get the user from the database"""
        result = self.db.query(f"SELECT * FROM users WHERE email='{email}' AND password='{password}';")
        if result:
            return User(**result)
