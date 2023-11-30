import time

from fastapi import APIRouter, status, WebSocket, WebSocketDisconnect, WebSocketException
from icecream import ic
from starlette.responses import HTMLResponse

from src.domain.game.game_state import GameState
from src.domain.game.schemes import ActiveGamesResponses
from src.infrastructure.core.websocket_manager_impl import ws_manager
from src.infrastructure.core.websocket_manager_waiting_room import ws_manager_waiting_room
from src.infrastructure.game.game_facade_impl import GameFacadeImpl

router = APIRouter(tags=['game'],
                   responses={status.HTTP_400_BAD_REQUEST: {"description": "Not found"}})

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var gameId = "007";  // Set the desired game ID
            var ws = new WebSocket(`ws://192.168.1.71:8000/ws/v1/game/${gameId}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages');
                var message = document.createElement('li');
                var data = JSON.parse(event.data)
                console.log(data)
                var match = data.match;
                var status = data.status;
                if(status) {
                    console.log(status)
                    var content = document.createTextNode(status);
                    message.appendChild(content);
                    messages.appendChild(message);
                }
                if(match) {
                    var content = document.createTextNode(match);
                    message.appendChild(content);
                    messages.appendChild(message);
                }

            };

            function sendMessage(event) {
                var input = document.getElementById("messageText");
                var message = { "message": input.value };
                ws.send(JSON.stringify(message));
                input.value = "";
                event.preventDefault();
            }
        </script>
    </body>
</html>
"""


@router.get("/")
async def get():
    return HTMLResponse(html)


@router.websocket('/ws/v1/waiting_rooms')
async def websocket_game_endpoint(websocket: WebSocket):
    await ws_manager_waiting_room.connect(websocket)
    active_games = ws_manager.active_games
    active_games_responses = ActiveGamesResponses(response=active_games)
    await ws_manager_waiting_room.broadcast(active_games_responses.model_dump_json())
    try:
        while True:
            data = await websocket.receive_json()
            ic(data)
            ic(type(data))
            active_games = ws_manager.active_games
            active_games_responses = ActiveGamesResponses(response=active_games)
            ic(active_games_responses)
            await ws_manager_waiting_room.broadcast(active_games_responses.model_dump_json())
    except WebSocketDisconnect:
        ic('exept')
        active_games = ws_manager.active_games
        active_games_responses = ActiveGamesResponses(response=active_games)
        ws_manager_waiting_room.disconnect(websocket)
        await ws_manager_waiting_room.broadcast(active_games_responses.model_dump_json())
    except TypeError as e:
        ic(e)
    finally:
        ic('finally')
        # active_games = ws_manager.active_games
        # active_games_responses = ActiveGamesResponses(response=active_games)
        # await ws_manager_waiting_room.broadcast(active_games_responses.model_dump_json())
        ws_manager_waiting_room.disconnect(websocket)



@router.websocket('/ws/v1/game/{game_id}')
async def websocket_game_endpoint(websocket: WebSocket, game_id: str):
    await websocket.accept()
    facade = GameFacadeImpl(ws_manager=ws_manager)
    # Create a new game
    game, player = await facade.create_or_join_game(game_id, websocket)
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
                    ic(game.winner_player)
                    facade.update_game_state(game, GameState.FINISH_GAME)
                    await facade.update_game(game_id, 'finish_game')
                    break
                next_player = game.get_inverse_player()
                game.set_current_player(next_player)
    except WebSocketDisconnect:
        await facade.update_game(game_id, 'disconnect_player')
        await facade.ws_manager.disconnect(game_id, websocket)
        ic('Disconnect Player!')
    except TypeError as e:
        ic(e)
    finally:
        await facade.ws_manager.disconnect(game_id, websocket)
