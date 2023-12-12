from pydantic import BaseModel, validate_call
from abc import ABC, abstractmethod

from src.domain.auth.i_auth_handler import IAuthHandler
from src.domain.auth.schemas import SchemaSignin, SchemaLogIn


class IAuthFacade(BaseModel, ABC):

    @abstractmethod
    @validate_call()
    def signin(self, email: str, password: str, auth_handler: IAuthHandler) -> SchemaSignin:
        """Create a new user in the database."""

    @abstractmethod
    @validate_call()
    def login(self, email: str, password: str, auth_handler: IAuthHandler) -> SchemaLogIn:
        """ Log the user in their account."""
