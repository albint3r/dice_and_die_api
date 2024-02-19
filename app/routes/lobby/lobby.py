from fastapi import APIRouter, WebSocket

from app.infrastructure.core.game_websocket_manager import game_websocket_manger
from app.infrastructure.lobby.lobby_use_case import LobbyUseCase
from app.infrastructure.lobby.lobby_websocket_manager import lobby_websocket_manager

router = APIRouter(prefix='/lobby/v1', tags=['lobby'])


@router.websocket('/games')
async def games_lobby(websocket: WebSocket):
    """This creates a connection with the current playing games"""
    lobby_use_case = LobbyUseCase(lobby_websocket_manager=lobby_websocket_manager,
                                  game_websocket_manager=game_websocket_manger)

    await lobby_use_case.subscribe_user(websocket)
    # After the user connect to the pool connections update their game status broadcasting the active games.
    await lobby_use_case.update_lobby_information()
    while True:
        await lobby_use_case.get_player_request_event(websocket)
        await lobby_use_case.update_lobby_information()
