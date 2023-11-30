from fastapi import WebSocket
from pydantic import BaseModel

from src.domain.game.game import Game


class _WebsocketManagerWaitingRoom(BaseModel):
    active_connections: list[WebSocket] = []

    class Config:
        arbitrary_types_allowed = True

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, games: dict[str, Game]):
        result = {'status': games}
        for connection in self.active_connections:
            await connection.send_json(result)


ws_manager_waiting_room = _WebsocketManagerWaitingRoom()
