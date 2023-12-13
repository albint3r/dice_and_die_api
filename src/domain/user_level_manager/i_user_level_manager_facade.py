from abc import ABC, abstractmethod

from pydantic import BaseModel, validate_call

from src.domain.auth.user import User
from src.domain.core.i_game_manager import IGameManager


class IUserLevelManagerFacade(BaseModel, ABC):

    @abstractmethod
    @validate_call()
    def update_user_level(self, user: User, exp_points: int, config_manager: IGameManager,
                          rank_manager: IGameManager) -> User:
        """Update the user experience points"""
