from abc import ABC, abstractmethod

from pydantic import BaseModel

from app.domain.auth.schemas.response import ResponseLogIn, ResponseSignin, ResponseUpdateUserNameAndLastName, \
    ResponseUsersRanking
from src.domain.auth.i_auth_handler import IAuthHandler


class IAuthUseCase(BaseModel, ABC):

    @abstractmethod
    def signin(self, email: str, password: str, auth_handler: IAuthHandler) -> ResponseSignin:
        """Create a new user in the database."""

    @abstractmethod
    def login(self, email: str, password: str, auth_handler: IAuthHandler) -> ResponseLogIn:
        """ Log the user in their account."""

    @abstractmethod
    def login_from_session_token(self, user_id: str, auth_handler: IAuthHandler) -> ResponseLogIn:
        """ Log from the session token. This happens when the user return to their account."""

    @abstractmethod
    def update_user_name_and_last_name(self,
                                       user_id: str,
                                       name: str,
                                       last_name: str) -> ResponseUpdateUserNameAndLastName:
        """Update in the db the name and last name of the user id."""

    @abstractmethod
    def get_users_ranking(self) -> ResponseUsersRanking:
        """Get the user sort by the user level and exp points"""
