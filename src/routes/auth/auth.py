from fastapi import APIRouter, status, WebSocket, WebSocketDisconnect
from icecream import ic
from mysql import connector

router = APIRouter(tags=['auth'],
                   responses={status.HTTP_400_BAD_REQUEST: {"description": "Not found"}})


@router.get('/')
def index():
    connection = connector.connect(user="root", password="t0b3t0t4l",
                                   host='db', database='dice_and_die',
                                   port='3306', auth_plugin='mysql_native_password')
    connection.cursor()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users;')
    users = cursor.fetchall()
    ic(users)
    return 'Hola Mundo'
