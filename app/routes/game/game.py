from fastapi import APIRouter, WebSocket
from icecream import ic

from app.infrastructure.core.game_websocket_manager import game_websocket_manger
from app.infrastructure.game.game_use_case import GameUseCase

router = APIRouter(tags=['game'], prefix='/v2')


@router.websocket('/game/{game_id}/{user_id}')
async def play_game(websocket: WebSocket, game_id: str, user_id: str):
    """This is the websocket endpoint to play the dice and die game"""
    game_use_case = GameUseCase(websocket_manager=game_websocket_manger)
    game, player = await game_use_case.create_or_join_game(game_id=game_id, user_id=user_id, websocket=websocket)
    await game_use_case.execute(game)
    ic(game)
    while game.is_waiting_opponent or not game.is_finished:
        request = await game_use_case.get_player_request_event(websocket)
        ic(request)
        if game.current_player.is_player_turn(player) and request.message == 'ok':
            ic(player)
    await websocket.close()
