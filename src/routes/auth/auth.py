from fastapi import APIRouter, status
from icecream import ic
from src.db.db import db

router = APIRouter(tags=['auth'],
                   responses={status.HTTP_400_BAD_REQUEST: {"description": "Not found"}})


@router.get('/')
def index():
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM users;')
    users = cursor.fetchall()
    ic(users)
    return 'Hola Mundo'
