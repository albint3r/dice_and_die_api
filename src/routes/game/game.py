from fastapi import APIRouter, status, WebSocket
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
            var ws = new WebSocket(`ws://192.168.1.71:8000/ws/v1/game/${userId}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages');
                var message = document.createElement('li');
                var match = JSON.parse(event.data).match;
                var content = document.createTextNode(match);
                message.appendChild(content);
                messages.appendChild(message);
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


@router.websocket('/ws/v1/game/{game_id}')
async def websocket_game_endpoint(websocket: WebSocket, game_id: str):
    facade = GameFacadeImpl(ws_manager=ws_manager)
    await websocket.accept()
    game = facade.ws_manager.get_match(game_id)
    # Create a new game if it not exists
    if not game:
        game = facade.new_game()
    await facade.ws_manager.connect(game_id, game, websocket)
    while True:
        json = await websocket.receive_json()
        ic(facade.select_column(json))
        await ws_manager.send_message(game_id, json)
