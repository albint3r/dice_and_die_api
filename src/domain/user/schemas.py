from fastapi import status
from pydantic import BaseModel

from src.domain.auth.user import User
from src.domain.user.user_rank import UserRank


class SchemaUpdateUserNameAndLastName(BaseModel):
    """Schema SignIn Responses"""
    user: User
    status_code: int = status.HTTP_202_ACCEPTED


class SchemaUsersRanks(BaseModel):
    """Schema SignIn Responses"""
    users_ranks: list[UserRank]
    status_code: int = status.HTTP_200_OK


class NameAndLastNameRequest(BaseModel):
    """Schema SignIn Responses"""
    name: str
    last_name: str
