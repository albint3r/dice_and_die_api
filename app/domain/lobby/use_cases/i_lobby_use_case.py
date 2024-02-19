from pydantic import BaseModel
from abc import ABC, abstractmethod

from app.domain.core.i_game_websocket_manager import IGameWebSocketManager
from app.domain.lobby.schemas.response import (ResponseActiveGames, ResponseTotalConnectedUsers)


class ILobbyUseCase(BaseModel, ABC):
    """This is the Lobby UseCase"""
    websocket_manager: IGameWebSocketManager

    @abstractmethod
    def get_active_games(self) -> ResponseActiveGames:
        """Get all the active games"""

    @abstractmethod
    def get_total_connected_users(self) -> ResponseTotalConnectedUsers:
        """Get the total user in the lobby connected"""
