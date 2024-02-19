from pydantic import BaseModel
from fastapi import status
from app.domain.core.ref_types import TActiveGames


class ResponseActiveGames(BaseModel):
    response: TActiveGames
    status_code: int = status.HTTP_200_OK


class ResponseTotalConnectedUsers(BaseModel):
    total: int
    status_code: int = status.HTTP_200_OK
