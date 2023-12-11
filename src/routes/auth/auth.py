from fastapi import APIRouter, status

from src.db.db import db
from src.infrastructure.auth.auth_facade_impl import AuthFacadeImpl
from src.repositories.auth.auth_repository import AuthRepository

router = APIRouter(tags=['auth'],
                   responses={status.HTTP_400_BAD_REQUEST: {"description": "Not found"}})

facade = AuthFacadeImpl(repo=AuthRepository(db=db))


@router.get('/')
def index():
    user = facade.signin('fake_user1@gmail.com', 'FAKE_PASSWORD')
    return user
