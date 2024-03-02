from datetime import datetime, timedelta
from typing import Final

from icecream import ic
from starlette.websockets import WebSocket

from app.domain.core.ref_types import TActiveGames
from app.domain.lobby.entities.lobby import Lobby
from app.domain.lobby.schemas.response import ResponseLobbyInformation
from app.domain.lobby.use_cases.i_lobby_websocket_manager import ILobbyWebSocketManager
from app.infrastructure.logs.logger import logger_conf


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
        for user_id, connection in self.active_connections.items():
            try:
                ws = list(connection.keys())[0]
                await ws.send_json(json_response)
                # Update the time of the user after create or join a game.
                self.active_connections[user_id] = {ws: datetime.now()}
            except Exception as e:
                logger_conf.log_send_websocket_json(json_response, e)

    def get_total_connected_users(self) -> int:
        return len(self.active_connections)

    async def check_inactive_connections(self) -> None:
        current_time = datetime.now()
        inactive_connections: list[tuple[str, WebSocket]] = []
        for user_id, socket_and_time in self.active_connections.items():
            ws = list(socket_and_time.keys())[0]
            last_activity = list(socket_and_time.values())[0]
            if current_time - last_activity > timedelta(seconds=3):
                inactive_connections.append((user_id, ws))
        for uid, websocket in inactive_connections:
            await websocket.close()
            del self.active_connections[uid]
            await logger_conf.log_inactive_connections(uid)
            ic('Connection succefully disconnected for inactivity.')


lobby_websocket_manager: Final[ILobbyWebSocketManager] = _LobbyWebSocketManager()
