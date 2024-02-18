from fastapi import APIRouter, WebSocket
from icecream import ic

from app.domain.game.enums.game_event import GameEvent
from app.domain.game.enums.game_state import GameState
from app.infrastructure.core.game_websocket_manager import game_websocket_manger
from app.infrastructure.game.game_use_case import GameUseCase

router = APIRouter(tags=['game'], prefix='/v2')


@router.websocket('/game/{game_id}/{user_id}')
async def play_game(websocket: WebSocket, game_id: str, user_id: str):
    """This is the websocket endpoint to play the dice and die game"""
    game_use_case = GameUseCase(websocket_manager=game_websocket_manger)
    game, player = await game_use_case.create_or_join_game(game_id=game_id, user_id=user_id, websocket=websocket)
    await game_use_case.execute(game)
    while game.is_waiting_opponent or not game.is_finished:
        request = await game_use_case.get_player_request_event(websocket)
        ic(player.user.name)
        game_use_case.verbose(game)
        if game.current_player and game.current_player.is_player_turn(player) and request.event == GameEvent.ROLL:
            # This part execute the [ROLL_DICE] event
            await game_use_case.execute(game)
            while game.state != GameState.CHANGE_CURRENT_PLAYER:
                # In this part normally occur the next events: [SELECT_COLUMN], [ADD_DICE], [DESTROY_OPPONENT_COLUMN] AND
                # [UPDATE_PLAYER_POINTS]. This while loop is mainly to check the user select a valid COLUMN.
                game_use_case.verbose(game)
                request = await game_use_case.get_player_request_event(websocket)
                await game_use_case.execute(game, selected_column=request)
                game_use_case.verbose(game)
            # This last execute is mainly responsible from the [CHANGE_CURRENT_PLAYER] OR [FINISH_GAME] event
            await game_use_case.execute(game)

    await websocket.close()
