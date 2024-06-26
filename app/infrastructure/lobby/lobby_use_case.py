from pydantic import ValidationError
from starlette.websockets import WebSocket

from app.domain.lobby.errors.errors import InvalidRequestUserLobby
from app.domain.lobby.schemas.request import LobbyEventRequest
from app.domain.lobby.use_cases.i_lobby_use_case import ILobbyUseCase


class LobbyUseCase(ILobbyUseCase):

    async def unsubscribe_user(self, user_id: str, websocket: WebSocket) -> None:
        await self.lobby_websocket_manager.disconnect(user_id)

    async def subscribe_user(self, user_id: str, websocket: WebSocket) -> None:
        await self.lobby_websocket_manager.connect(user_id, websocket)

    async def update_lobby_information(self) -> None:
        active_games = self.game_websocket_manager.active_games
        await self.lobby_websocket_manager.broadcast(active_games)

    async def get_player_request_event(self, user_id: str, websocket: WebSocket) -> LobbyEventRequest:
        try:
            response = await websocket.receive_json()
            return LobbyEventRequest(**response)
        except ValidationError as e:
            msg = (f'Request User Lobby Error Validator. User Client send invalid json request. '
                   f'Disconnect user to prevent malicious behavior: {e}')
            await self.lobby_websocket_manager.disconnect(user_id)
            raise InvalidRequestUserLobby(msg)
