from starlette.websockets import WebSocket

from app.domain.lobby.use_cases.i_lobby_use_case import ILobbyUseCase


class LobbyUseCase(ILobbyUseCase):

    async def subscribe_user(self, websocket: WebSocket) -> None:
        await self.lobby_websocket_manager.connect(websocket)

    async def update_lobby_information(self) -> None:
        active_games = self.game_websocket_manager.active_games
        await self.lobby_websocket_manager.broadcast(active_games)

    async def get_player_request_event(self, websocket: WebSocket) -> None:
        _ = await websocket.receive_json()
