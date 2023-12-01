from abc import ABC, abstractmethod

from pydantic import BaseModel

from src.domain.game.schemes import ActiveGamesResponses
from src.infrastructure.core.websocket_manager_impl import _WsManagerImpl


class IWaitingRoomFacade(ABC, BaseModel):

    @abstractmethod
    def getActiveResponses(self, ws_manager: _WsManagerImpl) -> ActiveGamesResponses:
        """Get Active Responses WebSockets in the Waiting Room"""
