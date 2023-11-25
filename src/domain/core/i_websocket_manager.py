from abc import ABC, abstractmethod
from typing import Dict, Set, Any

from fastapi import WebSocket
from pydantic import BaseModel

from src.domain.game.game import Game

# This is the typing of the active connections
TActiveGamesConnections = Dict[str, Set[WebSocket]]
TActiveMatches = Dict[str, Game]
# Payload message
TMessagePayload = Any


class IWsManager(ABC, BaseModel):

    @property
    @abstractmethod
    def active_connection(self) -> TActiveGamesConnections:
        """Get the Websocket active connections"""

    @property
    @abstractmethod
    def active_matches(self) -> TActiveMatches:
        """Get the Websocket active connections"""

    @abstractmethod
    def get_match(self, game_id: str) -> Game:
        """Return the current playing game"""

    @abstractmethod
    async def connect(self, game_id: str, game: Game, ws: WebSocket):
        """Connect with a new chanel"""

    @abstractmethod
    async def disconnect(self, game_id: str, ws: WebSocket):
        """Disconnect from chanel"""

    @abstractmethod
    async def send_message(self, game_id: str, message: TMessagePayload):
        """Send the message to the channel"""
