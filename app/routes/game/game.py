from fastapi import APIRouter, WebSocket, WebSocketDisconnect, WebSocketException, status
from icecream import ic

from app.db.db import db
from app.domain.game.enums.game_event import GameEvent
from app.domain.game.enums.game_state import GameState
from app.infrastructure.game.game_use_case import GameUseCase
from app.infrastructure.game.game_websocket_manager import game_websocket_manger
from app.infrastructure.game.level_use_case import LevelUserCase
from app.infrastructure.game.manager_leveling_use_case import ManagerLevelingUseCase
from app.infrastructure.game.rank_use_case import RankUseCase
from app.repositories.auth.auth_repository import AuthRepository

router = APIRouter(tags=['game'], prefix='/v2')


@router.websocket('/error')
async def error_socket(websocket: WebSocket):
    await websocket.accept()
    raise WebSocketException(reason='ESTO ES UNA SUPER PRUEBA', code=status.WS_1000_NORMAL_CLOSURE)


@router.websocket('/game/{game_id}/{user_id}')
async def play_game(websocket: WebSocket, game_id: str, user_id: str):
    """This is the websocket endpoint to play the dice and die game"""
    leveling_manager = ManagerLevelingUseCase(leve_manager=LevelUserCase(), rank_manager=RankUseCase())
    game_use_case = GameUseCase(websocket_manager=game_websocket_manger, leveling_manager=leveling_manager,
                                repo=AuthRepository(db=db))
    game, player = await game_use_case.create_or_join_game(game_id=game_id, user_id=user_id, websocket=websocket)
    try:
        await game_use_case.execute(game)
        while not game.is_finished or game.is_waiting_opponent:
            request = await game_use_case.get_player_request_event(websocket)
            ic(player.user.name)
            # game_use_case.verbose(game)
            if game.current_player and game.current_player.is_player_turn(player) and request.event == GameEvent.ROLL:
                # This part execute the [ROLL_DICE] event
                await game_use_case.execute(game)
                while game.state != GameState.CHANGE_CURRENT_PLAYER and game.state != GameState.FINISH_GAME:
                    # In this part normally occur the next events: [SELECT_COLUMN], [ADD_DICE], [DESTROY_OPPONENT_COLUMN] AND
                    # [UPDATE_PLAYER_POINTS]. This while loop is mainly to check the user select a valid COLUMN.
                    game_use_case.verbose(game)
                    request = await game_use_case.get_player_request_event(websocket)
                    await game_use_case.execute(game, selected_column=request)
                    game_use_case.verbose(game)
                # This last execute is mainly responsible from the [CHANGE_CURRENT_PLAYER] OR [FINISH_GAME] event
                await game_use_case.execute(game)
                game_use_case.verbose(game)
        ic(game)
        await websocket.close()
    except WebSocketDisconnect:
        await game_use_case.get_winner_after_player_disconnect(disconnected_player=player,
                                                               game=game, websocket=websocket)
        ic(f'Player: {player.user.name} is disconnected.')
        ic(game.winner_player)
