from abc import ABC, abstractmethod

from pydantic import BaseModel, validate_call

from src.domain.auth.user import User
from src.infrastructure.user_level_manager.user_level_manager import GameManager


class IUserLevelManagerFacade(BaseModel, ABC):

    @abstractmethod
    @validate_call()
    def update_user_level(self, user: User, exp_points: int, config_manager: GameManager) -> User:
        """Update the user experience points"""
