from fastapi import APIRouter, status, WebSocket, WebSocketDisconnect, WebSocketException
from icecream import ic

from src.db.db import db
from src.domain.game.game_state import GameState
from src.infrastructure.core.websocket_manager_impl import ws_manager
from src.infrastructure.game.game_facade_impl import GameFacadeImpl
from src.repositories.auth.auth_handler_impl import auth_handler
from src.repositories.auth.auth_repository import AuthRepository

router = APIRouter(tags=['game'],
                   responses={status.HTTP_400_BAD_REQUEST: {"description": "Not found"}})


@router.websocket('/ws/v1/game/{game_id}/{session_token}')
async def websocket_game_endpoint(websocket: WebSocket, game_id: str, session_token: str):
    user_id = auth_handler.decode_token(session_token)
    if not user_id:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="User don't provide Session Token")
    await websocket.accept()
    facade = GameFacadeImpl(ws_manager=ws_manager, repo=AuthRepository(db=db))
    # Create a new game
    game, player = await facade.create_or_join_game(game_id, user_id, websocket)
    try:
        while game.is_waiting_player or not game.is_finish:
            await facade.update_game(game_id, 'roll_dice')
            message = await facade.get_player_event_message(websocket)
            # Player Can interact?
            # This could be temporal until I deside how the player would take the turn
            if game.is_player_turn(player) and message == 'ok':
                game.current_player.roll_dice()
                facade.update_game_state(game, GameState.SELECT_COLUMN)
                await facade.update_game(game_id, 'select_column')
                ic(game.current_player.die_result)
                while True:
                    json_data = await websocket.receive_json()
                    col_index = facade.select_column(json_data)
                    ic(col_index)
                    if col_index and game.current_player.can_add_to_board_col(col_index):
                        die_val = game.current_player.die_result
                        if game.can_destroy_opponent_target_column(col_index, die_val):
                            game.destroy_opponent_target_column(col_index, die_val)
                            facade.update_game_state(game, GameState.DESTROY_OPPONENT_TARGET_COLUMN)
                            await facade.update_game(game_id, 'destroy_opponent_target_column')
                        game.current_player.add_dice_in_board_col(col_index, die_val)
                        facade.update_game_state(game, GameState.ADD_DICE_TO_COLUMN)
                        await facade.update_game(game_id, 'add_dice_to_colum')
                        break
                game.update_players_points(col_index)
                # facade.update_game_state(game, GameState.UPDATE_PLAYERS_POINTS)
                facade.update_game_state(game, GameState.ROLL_DICE)
                await facade.update_game(game_id, 'update_players_points')
                if game.is_finish:
                    facade.get_winner_player(game_id)
                    facade.update_game_state(game, GameState.FINISH_GAME)
                    await facade.update_game(game_id, 'finish_game')
                    await facade.ws_manager.disconnect(game_id, websocket)
                    break
                next_player = game.get_inverse_player()
                game.set_current_player(next_player)
    except WebSocketDisconnect:
        await facade.ws_manager.disconnect(game_id, websocket)
        ic('Disconnect Player!')
    except TypeError as _:
        # This happens only to the user that leave the match
        await facade.get_winner_after_player_disconnect(player, game, game_id, websocket)
        ic('GAME MATCH', player)
