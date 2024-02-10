from fastapi import APIRouter, status, Depends, HTTPException

from src.db.db import db
from src.domain.user.schemas import NameAndLastNameRequest, SchemaUpdateUserNameAndLastName, SchemaUsersRanks
from src.infrastructure.user.user_facade_impl import UserFacadeImpl
from src.repositories.auth.auth_handler_impl import auth_handler
from src.repositories.auth.auth_repository import AuthRepository
from src.repositories.user.user_repository import UserRepository

router = APIRouter(
    prefix='/user',
    tags=['user'],
    responses={
        status.HTTP_201_CREATED: {"description": "Success Create User"},
        status.HTTP_202_ACCEPTED: {"description": "Email and Password correct"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalide token"},
        status.HTTP_409_CONFLICT: {"description": "Email or Password error."},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"}
    })

facade = UserFacadeImpl(repo=UserRepository(db=db), repo_auth=AuthRepository(db=db))


@router.put('/v1/update', status_code=status.HTTP_201_CREATED)
def update_user_name_and_last_name(form_data: NameAndLastNameRequest,
                                   user_id: str = Depends(
                                       auth_handler.auth_wrapper)) -> SchemaUpdateUserNameAndLastName:
    try:
        return facade.update_user_name_and_last_name(user_id,
                                                     form_data.name,
                                                     form_data.last_name)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')


@router.get('/v1/ranks', status_code=status.HTTP_200_OK)
def get_user_name_and_last_name(_: str = Depends(auth_handler.auth_wrapper)) -> SchemaUsersRanks:
    try:
        return facade.get_users_ranking()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
