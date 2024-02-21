from typing import Final

from starlette.websockets import WebSocket

from app.domain.core.ref_types import TExtras
from app.domain.game.use_cases.i_viewers_websocket_manager import IViewersWebSocketManager


class ViewersWebSocketManager(IViewersWebSocketManager):
    async def connect(self, game_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.setdefault(game_id, set()).add(websocket)

    async def disconnect(self, game_id: str, websocket: WebSocket) -> None:
        self.active_connections.get(game_id).remove(websocket)
        if not self.active_connections[game_id]:
            del self.active_connections[game_id]

    async def broadcast(self, game_id: str, message: str = '', extras: TExtras | None = None) -> None:
        pass


viewers_websocket_manager: Final[IViewersWebSocketManager] = ViewersWebSocketManager()
