from fastapi import APIRouter, status, WebSocket, WebSocketDisconnect
from icecream import ic
from starlette.responses import HTMLResponse

from src.domain.game.schemes import ActiveGamesResponses
from src.infrastructure.core.websocket_manager_impl import ws_manager
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


@router.get('/v1/waiting_rooms')
async def websocket_game_endpoint() -> ActiveGamesResponses:
    active_games = ws_manager.active_games
    return ActiveGamesResponses(response=active_games)


@router.websocket('/ws/v1/game/{game_id}')
async def websocket_game_endpoint(websocket: WebSocket, game_id: str):
    await websocket.accept()
    facade = GameFacadeImpl(ws_manager=ws_manager)
    # Create a new game
    game, player = await facade.create_or_join_game(game_id, websocket)
    try:
        while game.is_waiting_player or not game.is_finish:
            await facade.update_game(game_id, 'start_new_round')
            message = await facade.get_player_event_message(websocket)
            # Player Can interact?
            # This could be temporal until I deside how the player would take the turn
            if game.is_player_turn(player) and message == 'ok':
                game.current_player.roll_dice()
                await facade.update_game(game_id, 'roll_dice')
                ic(game.current_player.die_result)
                while True:
                    json_data = await websocket.receive_json()
                    col_index = facade.select_column(json_data)
                    ic(col_index)
                    if col_index and game.current_player.can_add_to_board_col(col_index):
                        die_val = game.current_player.die_result
                        if game.can_destroy_opponent_target_column(col_index, die_val):
                            game.destroy_opponent_target_column(col_index, die_val)
                            await facade.update_game(game_id, 'destroy_opponent_target_column')
                        game.current_player.add_dice_in_board_col(col_index, die_val)
                        await facade.update_game(game_id, 'add_dice_to_colum')

                        break
                game.update_players_points(col_index)
                await facade.update_game(game_id, 'update_players_points')
                if game.is_finish:
                    facade.get_winner_player(game_id)
                    ic(game.winner_player)
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
