from abc import ABC, abstractmethod

from pydantic import BaseModel
from starlette.websockets import WebSocket

from app.domain.core.ref_types import TGamePlayer
from app.domain.game.entities.game import Game
from app.domain.game.schemas.request import ViewerRequest
from app.domain.game.use_cases.i_game_websocket_manager import IGameWebSocketManager
from app.domain.game.use_cases.i_viewers_websocket_manager import IViewersWebSocketManager


class IViewUseCase(BaseModel, ABC):
    websocket_manager: IGameWebSocketManager
    viewers_websocket_manager: IViewersWebSocketManager

    @abstractmethod
    async def execute(self, game: Game, websocket: WebSocket):
        """Viewers mian process"""

    @abstractmethod
    async def create_or_join(self, game_id: str, websocket: WebSocket) -> None:
        """Create or join view room"""

    @abstractmethod
    async def get_user_request_event(self, websocket: WebSocket) -> ViewerRequest:
        """Get the user request event"""
