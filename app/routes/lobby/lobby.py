from fastapi import APIRouter, status, WebSocket

router = APIRouter(
    prefix='/lobby/v1',
    tags=['lobby'],
    responses={
        status.HTTP_201_CREATED: {"description": "Success Create User"},
        status.HTTP_202_ACCEPTED: {"description": "Email and Password correct"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalide token"},
        status.HTTP_409_CONFLICT: {"description": "Email or Password error."},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"}
    })


@router.websocket('/lobby')
def games_lobby(websocket: WebSocket):
    """This creates a connection with the current playing games"""
