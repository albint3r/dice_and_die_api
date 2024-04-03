from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi_utilities import repeat_every
from icecream import ic

from app.infrastructure.auth.auth_handler_impl import token_ws_dependency
from app.infrastructure.game.game_websocket_manager import game_websocket_manger
from app.infrastructure.lobby.lobby_use_case import LobbyUseCase
from app.infrastructure.lobby.lobby_websocket_manager import lobby_websocket_manager

router = APIRouter(prefix='/v1/lobby', tags=['lobby'])


@router.on_event('startup')
@repeat_every(seconds=60)
async def check_inactive_connections():
    await lobby_websocket_manager.check_inactive_connections()


@router.get('/check-connection')
async def check_connections():
    ic(lobby_websocket_manager.active_connections)
    return {'ok': 200}


@router.get('/kill-connections')
async def kill_connections():
    lobby_websocket_manager.active_connections = {}
    return {'ok': 200, 'connections': lobby_websocket_manager.active_connections}


@router.websocket('/games')
async def get_lobby_games(websocket: WebSocket, user_id: token_ws_dependency):
    """This creates a connection with the current playing games"""
    lobby_use_case = LobbyUseCase(lobby_websocket_manager=lobby_websocket_manager,
                                  game_websocket_manager=game_websocket_manger)

    # After the user connect to the pool connections update their game status broadcasting the active games.
    try:
        await lobby_use_case.subscribe_user(user_id, websocket)
        await lobby_use_case.update_lobby_information()
        while True:
            await lobby_use_case.get_player_request_event(user_id, websocket)
            await lobby_use_case.update_lobby_information()
    except WebSocketDisconnect:
        await lobby_use_case.unsubscribe_user(user_id, websocket)
        await lobby_use_case.update_lobby_information()
        ic('Disconnect user from lobby')
