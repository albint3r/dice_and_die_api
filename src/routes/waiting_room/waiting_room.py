from fastapi import APIRouter, status, WebSocket, WebSocketDisconnect
from icecream import ic

from src.infrastructure.core.websocket_manager_impl import ws_manager
from src.infrastructure.waiting_room.waiting_room_facade_impl import WaitingRoomFacadeImpl
from src.infrastructure.waiting_room.websocket_manager_waiting_room import ws_manager_waiting_room

router = APIRouter(tags=['waiting_room'],
                   responses={status.HTTP_400_BAD_REQUEST: {"description": "Not found"}})


@router.websocket('/ws/v1/waiting_rooms')
async def websocket_game_endpoint(websocket: WebSocket):
    """This websocket get the active games and returned to all the listeners to update the waiting rooms"""
    await ws_manager_waiting_room.connect(websocket)
    facade = WaitingRoomFacadeImpl()
    active_games_responses = facade.getActiveResponses(ws_manager)
    await ws_manager_waiting_room.broadcast(active_games_responses.model_dump_json())
    try:
        while True:
            _ = await websocket.receive_json()
            active_games_responses = facade.getActiveResponses(ws_manager)
            await ws_manager_waiting_room.broadcast(active_games_responses.model_dump_json())
    except WebSocketDisconnect:
        ic('Except Waiting Room', websocket)
        active_games_responses = facade.getActiveResponses(ws_manager)
        ws_manager_waiting_room.disconnect(websocket)
        await ws_manager_waiting_room.broadcast(active_games_responses.model_dump_json())
    except TypeError as e:
        ic('WAITING ROOM', e, websocket)
    finally:
        ic('finally Waiting room', websocket)
        ws_manager_waiting_room.disconnect(websocket)
