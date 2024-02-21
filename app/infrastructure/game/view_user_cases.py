from datetime import datetime
from json import JSONDecodeError

from icecream import ic
from pydantic import ValidationError
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.domain.game.entities.game import Game
from app.domain.game.enums.viewer_event import ViewerEvent
from app.domain.game.errors.errors import MissingBroadcastGameInPlayersMatch
from app.domain.game.schemas.request import ViewerRequest
from app.domain.game.use_cases.i_view_use_case import IViewUseCase


class ViewUseCase(IViewUseCase):

    async def create_or_join(self, game_id: str, user_id: str, websocket: WebSocket) -> None:
        await self.viewers_websocket_manager.connect(game_id=game_id, websocket=websocket)
        game = self.websocket_manager.active_games.get(game_id)
        await self.viewers_websocket_manager.broadcast(game, message='join_viewer', extras={})
        try:
            while True:
                await self.execute(game, websocket)
        except MissingBroadcastGameInPlayersMatch:
            await websocket.close()
            await self.viewers_websocket_manager.disconnect(game_id, websocket)
        except WebSocketDisconnect:
            await self.viewers_websocket_manager.disconnect(game_id, websocket)
            ic('disconnect viewer')

    async def get_user_request_event(self, websocket: WebSocket) -> ViewerRequest:
        try:
            json_str = await websocket.receive_json()
            return ViewerRequest(**json_str)
        except ValidationError:
            return ViewerRequest(event=ViewerEvent.INVALID_INPUT_EVENT)
        except JSONDecodeError:
            return ViewerRequest(event=ViewerEvent.INVALID_INPUT_EVENT)

    async def execute(self, game: Game, websocket: WebSocket):
        request = await self.get_user_request_event(websocket)
        # Exist Game and is a valid input event?
        if request.event != ViewerEvent.INVALID_INPUT_EVENT:
            extras = {'viewer': request.event, 'time': datetime.now()}
            # Broadcast Viewer event to Players and Viewers
            await self.websocket_manager.broadcast(game_id=game.game_id, message='viewer_action', extras=extras)
            await self.viewers_websocket_manager.broadcast(game=game, message='viewer_action', extras=extras)
