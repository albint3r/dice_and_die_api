from abc import ABC, abstractmethod

from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel


class IAuthHandler(ABC, BaseModel):
    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def get_password_hash(self, password: str) -> bytes:
        """Receive a plain text password and hashed."""

    @abstractmethod
    def verify_password(self, password: str, hashed_password: bytes) -> bool:
        """Verify if the password is the same has the hashed password"""

    @abstractmethod
    def encode_token(self, user_id: str) -> str:
        """Create an encode token for the user."""

    @abstractmethod
    def decode_token(self, token_id: str) -> int:
        """Decode the user token"""

    @abstractmethod
    def auth_wrapper(self, auth: HTTPAuthorizationCredentials) -> int:
        """Is the auth handler to the routers"""

    @abstractmethod
    async def auth_websocket(self, **kwargs) -> str:
        """Is the auth handler for the websocket endpoints"""
