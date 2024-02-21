from abc import ABC, abstractmethod
from typing import Callable

from pydantic import BaseModel

from app.domain.game.entities.emote_message import EmoteMessage
from app.domain.game.entities.game import Game
from app.domain.game.entities.player import Player
from app.domain.game.schemas.request import GamePlayerRequest
from app.domain.game.use_cases.i_game_websocket_manager import IGameWebSocketManager
from app.domain.game.use_cases.i_viewers_websocket_manager import IViewersWebSocketManager


class IChatObserver(BaseModel, ABC):
    websockets_manager: IGameWebSocketManager
    viewers_websockets_manager: IViewersWebSocketManager

    @abstractmethod
    async def execute(self, emote_msg: EmoteMessage, game: Game, player: Player) -> None:
        """Execute Broadcast to all the active player"""

    @abstractmethod
    async def listen_request_event(self, request: GamePlayerRequest, game: Game, player: Player) -> None:
        """Listen all User Event to intercept Emotes messages"""
