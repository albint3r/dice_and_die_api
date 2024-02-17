from abc import ABC
from pydantic import BaseModel


class GameResponse(BaseModel, ABC):
    """This is the Base Game Response"""
