from fastapi import status
from pydantic import BaseModel

from app.domain.auth.entities.user import User
from app.domain.auth.entities.user_rank import UserRank


class ResponseSignin(BaseModel):
    """Schema SignIn Responses"""
    user: User
    session_token: str
    status_code: int = status.HTTP_201_CREATED


class ResponseLogIn(ResponseSignin):
    """Schema Login Responses"""
    status_code: int = status.HTTP_202_ACCEPTED


class ResponseUpdateUserNameAndLastName(BaseModel):
    """Schema SignIn Responses"""
    user: User
    status_code: int = status.HTTP_202_ACCEPTED


class ResponseUsersRanking(BaseModel):
    """Schema SignIn Responses"""
    users_ranks: list[UserRank]
    status_code: int = status.HTTP_200_OK
