from asyncio import sleep

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from icecream import ic

from app.domain.game.entities.player_rol import PlayerRol
from app.domain.game.enums.game_event import GameEvent
from app.domain.game.enums.game_state import GameState
from app.domain.game.schemas.request import GamePlayerRequest
from app.infrastructure.auth.auth_handler_impl import token_ws_dependency
from app.infrastructure.game.game_websocket_manager import game_websocket_manger
from app.infrastructure.game.viewers_websocket_manager import viewers_websocket_manager
from app.inyectables import pve_game_use_case_dependency, game_use_case_dependency, viewers_use_case_dependency, \
    chat_observer_dependency, adventure_game_mode_runner_dependency

router = APIRouter(tags=['game'], prefix='/v2')


@router.get('/check-connections')
async def check_active_connections():
    ic(game_websocket_manger.active_connections)
    ic(viewers_websocket_manager.active_connections)
    ic(game_websocket_manger.active_games)
    return {"ok": 200}


@router.websocket('/game/adventure')
async def play_adventure_game(websocket: WebSocket,
                              game_mode: adventure_game_mode_runner_dependency,
                              user_id: token_ws_dependency):
    game_id = 'FAKE_GAME_ID'
    game, player = await game_mode.create_or_join(game_id, user_id, websocket)
    try:
        while not game.config.is_game_mode_over:
            user_event_request = await game_mode.get_user_event_request(websocket)
            if game.current_player and game.current_player.is_player_turn(player) or game.state == GameState.REMATCH:
                await game_mode.play(game, player, user_event_request)
        await game_mode.get_overall_games_winner(game, player)
        await game_mode.end_game(game, websocket)
    except WebSocketDisconnect:
        await game_mode.get_winner_after_player_disconnect(disconnected_player=player,
                                                           game=game, websocket=websocket)


@router.websocket('/game/ai')
async def play_game_ai(websocket: WebSocket, game_use_case: pve_game_use_case_dependency, user_id: token_ws_dependency):
    game_id = game_use_case.get_valid_game_id('', '')
    game, player = await game_use_case.create_or_join(game_id=game_id, user_id=user_id, websocket=websocket)

    try:
        await game_use_case.execute(game)
        while not game.is_finished or game.is_waiting_opponent:
            request = await game_use_case.get_user_request_event(websocket)
            if game.current_player and game.current_player.is_player_turn(player) and request.event == GameEvent.ROLL:
                # This part execute the [ROLL_DICE] event
                await game_use_case.execute(game)
                while game.state != GameState.CHANGE_CURRENT_PLAYER and game.state != GameState.FINISH_GAME:
                    # In this part normally occur the next events: [SELECT_COLUMN], [ADD_DICE], [DESTROY_OPPONENT_COLUMN] AND
                    # [UPDATE_PLAYER_POINTS]. This while loop is mainly to check the user select a valid COLUMN.
                    request = await game_use_case.get_user_request_event(websocket)
                    await game_use_case.execute(game, selected_column=request)
                # This last execute is mainly responsible from the [CHANGE_CURRENT_PLAYER] OR [FINISH_GAME] event
                await game_use_case.execute(game)
            # This run the AI Part
            if game.current_player.rol == PlayerRol.AI:
                await sleep(1)
                await game_use_case.execute(game)
                ai_event = game_use_case.get_ai_selected_column(game)
                await sleep(1)
                await game_use_case.execute(game, selected_column=GamePlayerRequest(event=GameEvent(ai_event)))
                await game_use_case.execute(game)
        await game_use_case.websocket_manager.disconnect(game_id=game_id, websocket=websocket)
        await websocket.close()
    except WebSocketDisconnect:
        await game_use_case.websocket_manager.disconnect(game_id=game_id, websocket=websocket)


@router.websocket('/game/{game_id}')
async def play_game_pvp(websocket: WebSocket, game_id: str,
                        game_use_case: game_use_case_dependency,
                        view_use_case: viewers_use_case_dependency,
                        chat_observer: chat_observer_dependency,
                        user_id: token_ws_dependency):
    """This is the websocket endpoint to play the dice and die game"""

    # This validates if the user is creating or joining. If the game not exist is a dead game ID.
    game_id = game_use_case.get_valid_game_id(user_id, game_id)

    if game_use_case.websocket_manager.is_full(game_id):
        await view_use_case.create_or_join(game_id, user_id, websocket)
        return
    game, player = await game_use_case.create_or_join(game_id=game_id, user_id=user_id, websocket=websocket)

    try:
        await game_use_case.execute(game)
        while not game.is_finished or game.is_waiting_opponent:
            request = await game_use_case.get_user_request_event(websocket)
            await chat_observer.listen_request_event(request, game=game, player=player)
            if game.current_player and game.current_player.is_player_turn(player) and request.event == GameEvent.ROLL:
                # This part execute the [ROLL_DICE] event
                await game_use_case.execute(game)
                while game.state != GameState.CHANGE_CURRENT_PLAYER and game.state != GameState.FINISH_GAME:
                    # In this part normally occur the next events: [SELECT_COLUMN], [ADD_DICE], [DESTROY_OPPONENT_COLUMN] AND
                    # [UPDATE_PLAYER_POINTS]. This while loop is mainly to check the user select a valid COLUMN.
                    game_use_case.verbose(game)
                    request = await game_use_case.get_user_request_event(websocket)
                    await chat_observer.listen_request_event(request, game=game, player=player)
                    await game_use_case.execute(game, selected_column=request)
                    game_use_case.verbose(game)
                # This last execute is mainly responsible from the [CHANGE_CURRENT_PLAYER] OR [FINISH_GAME] event
                await game_use_case.execute(game)
                game_use_case.verbose(game)
        await websocket.close()
        await game_use_case.websocket_manager.disconnect(game_id=game_id, websocket=websocket)
    except WebSocketDisconnect:
        await game_use_case.get_winner_after_player_disconnect(disconnected_player=player,
                                                               game=game, websocket=websocket)
