from abc import ABC, abstractmethod
from pydantic import BaseModel


class IScore(ABC, BaseModel):
    """This is just a Base Class to get the score of the board columns and Board"""

    @abstractmethod
    def get_result(self, **kwargs) -> int:
        """Get the score result"""
