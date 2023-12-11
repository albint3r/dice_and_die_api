from pydantic import BaseModel, validate_call
from abc import ABC, abstractmethod


class IAuthFacade(BaseModel, ABC):

    @abstractmethod
    @validate_call()
    def signin(self, email: str, password: str):
        """Create a new user in the database."""

    @abstractmethod
    @validate_call()
    def login(self, email: str, password: str):
        """ Log the user in their account."""

    @abstractmethod
    @validate_call()
    def logout(self):
        """Disconnect the user of the current session."""
