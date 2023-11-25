from starlette.websockets import WebSocket

from src.domain.core.i_websocket_manager import IWsManager, TMessagePayload, TActiveConnections


class WsManagerImpl(IWsManager):
    _active_connection: TActiveConnections = {}

    @property
    def active_connection(self) -> TActiveConnections:
        return self._active_connection

    async def connect(self, game_id: str, ws: WebSocket):
        self._active_connection.setdefault(game_id, set()).add(ws)

    async def disconnect(self, game_id: str, ws: WebSocket):
        self._active_connection[game_id].remove(ws)

    async def send_message(self, game_id: str, message: TMessagePayload):
        for ws in self._active_connection.get(game_id, []):
            await ws.send_json(message)
