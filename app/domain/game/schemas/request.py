from abc import ABC
from pydantic import BaseModel


class GameRequest(BaseModel, ABC):
    """This is the Base Game Request"""
