from pydantic import BaseModel, validate_call
from abc import ABC, abstractmethod

from src.domain.user.schemas import SchemaUpdateUserNameAndLastName, SchemaUsersRanks


class IUserFacade(BaseModel, ABC):

    @abstractmethod
    @validate_call()
    def update_user_name_and_last_name(self, user_id: str, name: str,
                                       last_name: str) -> SchemaUpdateUserNameAndLastName:
        """Update in the db the name and last name of the user id."""

    @abstractmethod
    @validate_call()
    def get_users_ranking(self) -> SchemaUsersRanks:
        """Get the user sort by the user level and exp points"""
