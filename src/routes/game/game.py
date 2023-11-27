import time

from fastapi import APIRouter, status, WebSocket, WebSocketDisconnect
from icecream import ic
from starlette.responses import HTMLResponse

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
            var userId = "007";  // Set the desired user ID
            var ws = new WebSocket(`ws://192.168.1.71:8000/ws/v1/game2/${userId}`);
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
                input.value = '';
                event.preventDefault();
            }
        </script>
    </body>
</html>
"""


@router.get("/")
async def get():
    return HTMLResponse(html)


@router.websocket('/ws/v1/game2/{game_id}')
async def websocket_game_endpoint2(websocket: WebSocket, game_id: str):
    await websocket.accept()
    facade = GameFacadeImpl(ws_manager=ws_manager)
    # Create a new game
    game = facade.get_game(game_id)
    if not facade.exist_game(game_id):
        # Create new game
        game = facade.new_game2()
        await facade.ws_manager.connect(game_id, game, websocket)
        # Create Player 1
        player = facade.new_player()
        facade.join_waiting_room(game_id, player)
        await ws_manager.send_message(game_id, 'Player 1 Connected')
    else:
        # Create player 2
        player = facade.new_player()
        if not facade.is_full_room(game_id):
            facade.join_waiting_room(game_id, player)
            # Select Player Start Order
            start_player = facade.select_player_start(game)
            game.set_current_player(start_player)
            await facade.ws_manager.connect(game_id, game, websocket)
            await ws_manager.send_message(game_id, 'Player 2 Connected')

    try:
        while game.is_waiting_player or not game.is_finish:
            json = await websocket.receive_json()
            # Player Can interact?
            if game.is_player_turn(player):
                ic(f'Player Name: {player.id}')
                ic(game.current_player)
    except WebSocketDisconnect:
        await ws_manager.send_message(game_id, 'DISCONNECTED PLAYER')
        await facade.ws_manager.disconnect(game_id, websocket)

# @router.websocket('/ws/v1/game/{game_id}')
# async def websocket_game_endpoint(websocket: WebSocket, game_id: str):
#     facade = GameFacadeImpl(ws_manager=ws_manager)
#     # Accept websocket connection
#     await websocket.accept()
#     game = facade.ws_manager.get_game(game_id)
#     ic(game)
#     # Create a new game if it not exists
#     if not game:
#         game = facade.new_game()
#         start_player = facade.select_player_start(game)
#         game.set_current_player(start_player)
#     await facade.ws_manager.connect(game_id, game, websocket)
#
#     ic('-------------------------INICIO-------------------------------------')
#     try:
#         while not game.is_finish:
#             ic(game.p1)
#             ic(game.p2)
#             game.current_player.roll_dice()
#             ic(f"Die result: {game.current_player.die_result}")
#             # Get user input
#             json = await websocket.receive_json()
#             col_index = facade.select_column(json)
#             is_game_full = facade.ws_manager.is_game_full(game_id)
#             if col_index and is_game_full:
#                 # TODO: here a need to validate the user is the same and check the value is correct type
#                 if game.current_player.can_add_to_board_col(col_index):
#                     die_val = game.current_player.die_result
#                     if game.can_destroy_opponent_target_column(col_index, die_val):
#                         game.destroy_opponent_target_column(col_index, die_val)
#                     game.current_player.add_dice_in_board_col(col_index, die_val)
#                     await ws_manager.send_match(game_id)
#
#                 game.update_players_points(col_index)
#                 next_player = game.get_inverse_player()
#                 game.set_current_player(next_player)
#                 await ws_manager.send_message(game_id, '-*' * 100)
#                 ic('-*' * 100)
#             else:
#                 await ws_manager.send_message(game_id, 'NO NUMBER')
#         ic('-*' * 100)
#         ic('-----------FINISH GAME------------------')
#         ic('-*' * 100)
#         await ws_manager.send_message(game_id, 'DISCONNECTED PLAYER')
#         await facade.ws_manager.disconnect(game_id, websocket)
#     except WebSocketDisconnect:
#         await ws_manager.send_message(game_id, 'DISCONNECTED PLAYER')
#         await facade.ws_manager.disconnect(game_id, websocket)
