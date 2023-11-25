from abc import ABC, abstractmethod
from typing import Dict, Set, Any

from fastapi import WebSocket
from pydantic import BaseModel, validate_call

# This is the typing of the active connections
TActiveConnections = Dict[str, Set[WebSocket]]
# Payload message
TMessagePayload = Any


class IWsManager(ABC, BaseModel):

    @property
    @abstractmethod
    def active_connection(self) -> TActiveConnections:
        """Get the Websocket active connections"""

    @abstractmethod
    @validate_call()
    async def connect(self, game_id: str, ws: WebSocket):
        """Connect with a new chanel"""

    @abstractmethod
    @validate_call()
    async def disconnect(self, game_id: str, ws: WebSocket):
        """Disconnect from chanel"""

    @abstractmethod
    @validate_call()
    async def send_message(self, game_id: str, message: TMessagePayload):
        """Send the message to the channel"""
