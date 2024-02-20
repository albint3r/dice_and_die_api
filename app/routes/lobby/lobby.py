from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from icecream import ic

from app.infrastructure.game.game_websocket_manager import game_websocket_manger
from app.infrastructure.lobby.lobby_use_case import LobbyUseCase
from app.infrastructure.lobby.lobby_websocket_manager import lobby_websocket_manager

router = APIRouter(prefix='/lobby/v1', tags=['lobby'])


@router.get('/check-connection')
async def check_connections():
    ic(lobby_websocket_manager.active_connections)
    return {'ok': 200}


@router.websocket('/games')
async def get_lobby_games(websocket: WebSocket):
    """This creates a connection with the current playing games"""
    lobby_use_case = LobbyUseCase(lobby_websocket_manager=lobby_websocket_manager,
                                  game_websocket_manager=game_websocket_manger)

    await lobby_use_case.subscribe_user(websocket)
    # After the user connect to the pool connections update their game status broadcasting the active games.
    await lobby_use_case.update_lobby_information()
    try:
        while True:
            await lobby_use_case.get_player_request_event(websocket)
            await lobby_use_case.update_lobby_information()
    except WebSocketDisconnect:
        await lobby_use_case.unsubscribe_user(websocket)
        await lobby_use_case.update_lobby_information()
        ic('Disconnect user')