import asyncio
from datetime import datetime
from typing import Final

from icecream import ic
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
            ws = list(self.active_connections[user_id].keys())[0]
            await ws.close()
        self.active_connections[user_id] = {websocket: datetime.now()}

    async def disconnect(self, user_id: str, websocket: WebSocket) -> None:
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def broadcast(self, active_games: TActiveGames) -> None:
        lobby = Lobby(active_games=active_games)
        response = ResponseLobbyInformation(lobby=lobby, total_players=self.get_total_connected_users())
        json_response = response.model_dump_json()
        for connection in self.active_connections.values():
            ws = list(connection.keys())[0]
            await ws.send_json(json_response)

    def get_total_connected_users(self) -> int:
        return len(self.active_connections)

    async def check_inactive_connections(self) -> None:
        while True:
            await asyncio.sleep(5)  # Revisar conexiones inactivas cada minuto
            current_time = datetime.now()
            ic(f'Hola mundo ->{current_time}')


lobby_websocket_manager: Final[ILobbyWebSocketManager] = _LobbyWebSocketManager()
