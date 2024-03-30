from asyncio import sleep

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from icecream import ic

from app.db.db import db
from app.domain.game.enums.game_event import GameEvent
from app.domain.game.enums.game_state import GameState
from app.domain.game.schemas.request import GamePlayerRequest
from app.infrastructure.auth.auth_handler_impl import auth_handler
from app.infrastructure.game.chat_observer import ChatObserver
from app.infrastructure.game.game_use_case import GameUseCase
from app.infrastructure.game.game_websocket_manager import game_websocket_manger
from app.infrastructure.game.level_use_case import LevelUserCase
from app.infrastructure.game.manager_leveling_use_case import ManagerLevelingUseCase
from app.infrastructure.game.pve_game_use_case import PVEGameUseCase
from app.infrastructure.game.rank_use_case import RankUseCase
from app.infrastructure.game.view_user_cases import ViewUseCase
from app.infrastructure.game.viewers_websocket_manager import viewers_websocket_manager
from app.repositories.auth.auth_repository import AuthRepository

router = APIRouter(tags=['game'], prefix='/v2')


@router.get('/check-connections')
async def check_active_connections():
    ic(game_websocket_manger.active_connections)
    ic(viewers_websocket_manager.active_connections)
    ic(game_websocket_manger.active_games)
    return {"ok": 200}


@router.websocket('/game/ai')
async def play_game_ai(websocket: WebSocket, user_id: str = Depends(auth_handler.auth_websocket)):
    repo = AuthRepository(db=db)
    leveling_manager = ManagerLevelingUseCase(leve_manager=LevelUserCase(), rank_manager=RankUseCase())
    leveling_manager._base_win_points = 0

    game_use_case = PVEGameUseCase(websocket_manager=game_websocket_manger,
                                   viewers_websocket_manager=viewers_websocket_manager,
                                   leveling_manager=leveling_manager, repo=repo)
    # We are going to use always a new game because we wanted the game is visible in the lobby but no playable for
    # other players. This creates a new room but because we are going to fill it with the AI  nobody would be entering.
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
                    game_use_case.verbose(game)
                    request = await game_use_case.get_user_request_event(websocket)
                    await game_use_case.execute(game, selected_column=request)
                    game_use_case.verbose(game)
                # This last execute is mainly responsible from the [CHANGE_CURRENT_PLAYER] OR [FINISH_GAME] event
                await game_use_case.execute(game)
                game_use_case.verbose(game)

            # This run the AI Part
            if game.current_player == game.p2:
                await sleep(1)
                await game_use_case.execute(game)
                ai_event = game_use_case.get_ai_selected_column(game)
                await sleep(1)
                await game_use_case.execute(game, selected_column=GamePlayerRequest(event=GameEvent(ai_event)))
                ic(game.p2)
                await game_use_case.execute(game)
                game_use_case.verbose(game)
        ic(game)
        await game_use_case.websocket_manager.disconnect(game_id=game_id, websocket=websocket)
        await websocket.close()
    except WebSocketDisconnect:
        await game_use_case.websocket_manager.disconnect(game_id=game_id, websocket=websocket)
        ic(f'Player: {player.user.name} is disconnected.')


@router.websocket('/game/{game_id}')
async def play_game_pvp(websocket: WebSocket, game_id: str, user_id: str = Depends(auth_handler.auth_websocket)):
    """This is the websocket endpoint to play the dice and die game"""
    repo = AuthRepository(db=db)
    leveling_manager = ManagerLevelingUseCase(leve_manager=LevelUserCase(), rank_manager=RankUseCase())
    game_use_case = GameUseCase(websocket_manager=game_websocket_manger,
                                viewers_websocket_manager=viewers_websocket_manager,
                                leveling_manager=leveling_manager, repo=repo)
    # This validates if the user is creating or joining. If the game not exist is a dead game ID.
    game_id = game_use_case.get_valid_game_id(user_id, game_id)

    if game_use_case.websocket_manager.is_full(game_id):
        view_use_case = ViewUseCase(websocket_manager=game_websocket_manger,
                                    viewers_websocket_manager=viewers_websocket_manager, repo=repo)

        await view_use_case.create_or_join(game_id, user_id, websocket)
        return
    game, player = await game_use_case.create_or_join(game_id=game_id, user_id=user_id, websocket=websocket)
    chat_observer = ChatObserver(viewers_websockets_manager=viewers_websocket_manager,
                                 websockets_manager=game_websocket_manger)
    try:
        await game_use_case.execute(game)
        while not game.is_finished or game.is_waiting_opponent:
            request = await game_use_case.get_user_request_event(websocket)
            await chat_observer.listen_request_event(request, game=game, player=player)
            ic(player.user.name)
            # game_use_case.verbose(game)
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
        ic(game)
        await websocket.close()
        await game_use_case.websocket_manager.disconnect(game_id=game_id, websocket=websocket)
    except WebSocketDisconnect:
        await game_use_case.get_winner_after_player_disconnect(disconnected_player=player,
                                                               game=game, websocket=websocket)
        ic(f'Player: {player.user.name} is disconnected.')
        ic(game.winner_player)
