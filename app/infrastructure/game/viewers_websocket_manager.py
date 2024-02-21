from typing import Final

from icecream import ic
from starlette.websockets import WebSocket

from app.domain.core.ref_types import TExtras
from app.domain.game.entities.game import Game
from app.domain.game.schemas.response import ResponseGame
from app.domain.game.use_cases.i_viewers_websocket_manager import IViewersWebSocketManager


class ViewersWebSocketManager(IViewersWebSocketManager):
    async def connect(self, game_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.setdefault(game_id, set()).add(websocket)

    async def disconnect(self, game_id: str, websocket: WebSocket) -> None:
        self.active_connections.get(game_id).remove(websocket)
        if not self.active_connections[game_id]:
            del self.active_connections[game_id]

    async def broadcast(self, game: Game, message: str = '', extras: TExtras | None = None) -> None:
        connections = self.active_connections.get(game.game_id)
        # Are viewer in the game?
        if connections:
            response = ResponseGame(game=game, message=message, extras=extras)
            jsons_response = response.model_dump_json()
            ic(connections)
            for viewer_connection in connections:
                await viewer_connection.send_json(jsons_response)


viewers_websocket_manager: Final[IViewersWebSocketManager] = ViewersWebSocketManager()
