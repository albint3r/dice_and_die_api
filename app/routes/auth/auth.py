from fastapi import APIRouter, status, Depends, HTTPException

from app.db.db import db
from app.domain.auth.schemas.request import RequestAuthEmail, RequestNameAndLastName
from app.domain.auth.schemas.response import (ResponseLogIn, ResponseSignin, ResponseUpdateUserNameAndLastName,
                                              ResponseUsersRanking, ResponseUserRank)
from app.infrastructure.auth.auth_handler_impl import auth_handler
from app.infrastructure.auth.auth_use_case import AuthUseCase
from app.repositories.auth.auth_repository import AuthRepository

router = APIRouter(
    prefix='/v2/auth',
    tags=['auth'],
    responses={
        status.HTTP_201_CREATED: {"description": "Success Create User"},
        status.HTTP_202_ACCEPTED: {"description": "Email and Password correct"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalide token"},
        status.HTTP_409_CONFLICT: {"description": "Email or Password error."},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"}
    })


@router.post('/signin', status_code=status.HTTP_201_CREATED)
async def signin_with_email_and_password(form_data: RequestAuthEmail) -> ResponseSignin:
    try:
        facade = AuthUseCase(repo=AuthRepository(db=db))
        return facade.signin(form_data.email, form_data.password.get_secret_value(), auth_handler)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')


@router.post('/login', status_code=status.HTTP_202_ACCEPTED)
async def login_with_email_and_password(form_data: RequestAuthEmail) -> ResponseLogIn:
    try:
        facade = AuthUseCase(repo=AuthRepository(db=db))
        return facade.login(form_data.email, form_data.password.get_secret_value(), auth_handler)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')


@router.post('/login/token', status_code=status.HTTP_202_ACCEPTED)
async def login_with_session_token(user_id: str = Depends(auth_handler.auth_wrapper)) -> ResponseLogIn:
    try:
        facade = AuthUseCase(repo=AuthRepository(db=db))
        return facade.login_from_session_token(user_id, auth_handler)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')


@router.put('/profile', status_code=status.HTTP_201_CREATED)
async def update_user_name_and_last_name(data: RequestNameAndLastName,
                                   user_id: str = Depends(
                                       auth_handler.auth_wrapper)) -> ResponseUpdateUserNameAndLastName:
    try:
        facade = AuthUseCase(repo=AuthRepository(db=db))
        return facade.update_user_name_and_last_name(user_id, data.name, data.last_name)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')


@router.get('/ranks', status_code=status.HTTP_200_OK)
async def get_users_ranking(_: str = Depends(auth_handler.auth_wrapper)) -> ResponseUsersRanking:
    try:
        facade = AuthUseCase(repo=AuthRepository(db=db))
        return facade.get_users_ranking()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')


@router.get('/ranks/user', status_code=status.HTTP_200_OK)
async def get_user_ranking(user_id: str = Depends(auth_handler.auth_wrapper)) -> ResponseUserRank:
    try:
        facade = AuthUseCase(repo=AuthRepository(db=db))
        return facade.get_user_ranking(user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')


@router.get('/ranks/category/{rank_id}', status_code=status.HTTP_200_OK)
async def get_users_ranking_by_rank(rank_id: int, _: str = Depends(auth_handler.auth_wrapper)) -> ResponseUsersRanking:
    try:
        facade = AuthUseCase(repo=AuthRepository(db=db))
        return facade.get_users_ranking_by_rank(rank_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')


@router.get('/ranks/category/{rank_id}/user', status_code=status.HTTP_200_OK)
async def get_user_ranking_by_rank(rank_id: int, user_id: str = Depends(auth_handler.auth_wrapper)) -> ResponseUserRank:
    try:
        facade = AuthUseCase(repo=AuthRepository(db=db))
        return facade.get_user_ranking_by_rank(rank_id=rank_id, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')


@router.post('/test', status_code=status.HTTP_200_OK)
async def test_route_token_session(user_id: str = Depends(auth_handler.auth_wrapper)):
    try:
        return user_id
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
