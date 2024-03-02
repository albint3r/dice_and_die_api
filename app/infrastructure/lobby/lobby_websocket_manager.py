from typing import Final

from starlette.websockets import WebSocket

from app.domain.core.ref_types import TActiveGames
from app.domain.lobby.entities.lobby import Lobby
from app.domain.lobby.schemas.response import ResponseLobbyInformation
from app.domain.lobby.use_cases.i_lobby_websocket_manager import ILobbyWebSocketManager


class _LobbyWebSocketManager(ILobbyWebSocketManager):

    async def connect(self, user_id: str, websocket: WebSocket) -> None:
        """This connection assure the user only have one connection."""
        await websocket.accept()
        if self.active_connections.get(user_id):
            await self.active_connections[user_id].close()
        self.active_connections[user_id] = websocket

    async def disconnect(self, user_id: str, websocket: WebSocket) -> None:
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def broadcast(self, active_games: TActiveGames) -> None:
        lobby = Lobby(active_games=active_games)
        response = ResponseLobbyInformation(lobby=lobby, total_players=self.get_total_connected_users())
        json_response = response.model_dump_json()
        for connection in self.active_connections.values():
            await connection.send_json(json_response)

    def get_total_connected_users(self) -> int:
        return len(self.active_connections)


lobby_websocket_manager: Final[ILobbyWebSocketManager] = _LobbyWebSocketManager()
