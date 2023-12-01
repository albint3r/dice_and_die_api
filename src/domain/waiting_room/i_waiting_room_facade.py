from abc import ABC, abstractmethod

from fastapi import WebSocket
from pydantic import BaseModel

from src.domain.game.schemes import ActiveGamesResponses
from src.infrastructure.core.websocket_manager_impl import _WsManagerImpl
from src.infrastructure.waiting_room.websocket_manager_waiting_room import _WebsocketManagerWaitingRoom


class IWaitingRoomFacade(ABC, BaseModel):

    @abstractmethod
    def getActiveResponses(self, ws_manager: _WsManagerImpl) -> ActiveGamesResponses:
        """Get Active Responses WebSockets in the Waiting Room"""

    @abstractmethod
    async def disconnect(self, websocket: WebSocket) -> None:
        """Get Active Responses WebSockets in the Waiting Room"""
