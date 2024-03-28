from pydantic import BaseModel
from abc import ABC, abstractmethod

from app.domain.analytics.entities.single_play_history import SinglePlayHistory


class IAnalyticsUseCase(BaseModel, ABC):

    @abstractmethod
    def get_plays_history(self) -> list[SinglePlayHistory]:
        """This return a list from single play history"""
