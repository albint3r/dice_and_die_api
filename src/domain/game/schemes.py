from abc import ABC
from pydantic import BaseModel
from fastapi import status

from src.domain.core.i_websocket_manager import TActiveMatches


class GameResponses(ABC, BaseModel):
    """This is the Base Model for the Game Response"""
    status_code: int


class ActiveGamesResponses(GameResponses):
    response: TActiveMatches
    status_code: int = status.HTTP_200_OK
