from typing import Final

from starlette.websockets import WebSocket

from app.domain.core.ref_types import TActiveGames
from app.domain.lobby.schemas.response import ResponseLobbyInformation
from app.domain.lobby.use_cases.i_lobby_websocket_manager import ILobbyWebSocketManager


class _LobbyWebSocketManager(ILobbyWebSocketManager):

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, active_games: TActiveGames) -> None:
        response = ResponseLobbyInformation(active_games=active_games, total_players=self.get_total_connected_users())
        json_response = response.model_dump_json()
        for connection in self.active_connections:
            await connection.send_json(json_response)

    def get_total_connected_users(self) -> int:
        return len(self.active_connections)


lobby_websocket_manager: Final[ILobbyWebSocketManager] = _LobbyWebSocketManager()
