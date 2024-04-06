from datetime import datetime
from json import JSONDecodeError

from icecream import ic
from pydantic import ValidationError, validate_call
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.domain.game.entities.game import Game
from app.domain.game.entities.viewer import Viewer
from app.domain.game.enums.viewer_event import ViewerEvent
from app.domain.game.errors.errors import MissingBroadcastGameInPlayersMatch
from app.domain.game.schemas.request import ViewerRequest
from app.domain.game.use_cases.i_view_use_case import IViewUseCase
from app.repositories.auth.auth_repository import AuthRepository


class ViewUseCase(IViewUseCase):
    repo: AuthRepository

    @validate_call(config=dict(arbitrary_types_allowed=True))
    async def create_or_join(self, game_id: str, user_id: str, websocket: WebSocket) -> None:
        user = self.repo.get_user_by_id(user_id)
        viewer = Viewer(user=user)
        game = self.websocket_manager.active_games.get(game_id)
        extras = {'viewer': viewer.model_dump_json()}
        await self.viewers_websocket_manager.connect(game_id, websocket)
        await self.viewers_websocket_manager.broadcast(game, message='join_viewer', extras=extras)
        try:
            while True:
                await self.execute(game, websocket)
        except MissingBroadcastGameInPlayersMatch:
            await websocket.close()
            await self.viewers_websocket_manager.disconnect(game_id, websocket)
        except WebSocketDisconnect:
            await self.viewers_websocket_manager.disconnect(game_id, websocket)
            ic('disconnect viewer')

    @validate_call(config=dict(arbitrary_types_allowed=True), validate_return=True)
    async def get_user_request_event(self, websocket: WebSocket) -> ViewerRequest:
        try:
            json_str = await websocket.receive_json()
            return ViewerRequest(**json_str)
        except ValidationError:
            return ViewerRequest(event=ViewerEvent.INVALID_INPUT_EVENT)
        except JSONDecodeError:
            return ViewerRequest(event=ViewerEvent.INVALID_INPUT_EVENT)

    @validate_call(config=dict(arbitrary_types_allowed=True))
    async def execute(self, game: Game, websocket: WebSocket) -> None:
        request = await self.get_user_request_event(websocket)
        # Exist Game and is a valid input event?
        if request.event != ViewerEvent.INVALID_INPUT_EVENT:
            extras = {'viewer': request.event, 'time': datetime.now()}
            message = 'viewer_action'
            # Broadcast Viewer event to Players and Viewers
            await self.websocket_manager.broadcast(game_id=game.game_id, message=message, extras=extras)
            await self.viewers_websocket_manager.broadcast(game=game, message=message, extras=extras)

    @validate_call(validate_return=True)
    def is_room_full(self, game_id: str) -> bool:
        return self.websocket_manager.is_full(game_id)
