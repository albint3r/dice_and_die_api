from fastapi import status
from pydantic import BaseModel

from app.domain.auth.entities.user import User


class ResponseSignin(BaseModel):
    """Schema SignIn Responses"""
    user: User
    session_token: str
    status_code: int = status.HTTP_201_CREATED


class ResponseLogIn(ResponseSignin):
    """Schema Login Responses"""
    status_code: int = status.HTTP_202_ACCEPTED
