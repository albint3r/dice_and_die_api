from fastapi import APIRouter, status, HTTPException
from icecream import ic

from app.domain.auth.schemas.request import UserUpdateNamesRequest, LoginRequest, SignInRequest, LogInWithGoogle
from app.domain.auth.schemas.response import (ResponseLogIn, ResponseSignin, ResponseUpdateUserNameAndLastName,
                                              ResponseUsersRanking, ResponseUserRank)
from app.infrastructure.auth.auth_handler_impl import auth_handler, token_http_dependency
from app.inyectables import auth_use_case_dependency

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


@router.post('/signin/google', status_code=status.HTTP_201_CREATED)
async def signin_with_google(data: LogInWithGoogle, facade: auth_use_case_dependency) -> ResponseSignin:
    try:
        return facade.signin_with_google(data.google_user_id, auth_handler)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{e}')


@router.post('/signin', status_code=status.HTTP_201_CREATED)
async def signin_with_email_and_password(form_data: SignInRequest, facade: auth_use_case_dependency) -> ResponseSignin:
    ic(form_data)
    try:
        return facade.signin(form_data.email, form_data.name, form_data.password.get_secret_value(), auth_handler)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')


@router.post('/login', status_code=status.HTTP_202_ACCEPTED)
async def login_with_email_and_password(form_data: LoginRequest, facade: auth_use_case_dependency) -> ResponseLogIn:
    try:
        return facade.login(form_data.email, form_data.password.get_secret_value(), auth_handler)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')


@router.post('/login/token', status_code=status.HTTP_202_ACCEPTED)
async def login_with_session_token(facade: auth_use_case_dependency, user_id: token_http_dependency) -> ResponseLogIn:
    try:
        return facade.login_from_session_token(user_id, auth_handler)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')


@router.put('/profile', status_code=status.HTTP_201_CREATED)
async def update_user_name_and_last_name(data: UserUpdateNamesRequest,
                                         facade: auth_use_case_dependency,
                                         user_id: token_http_dependency) -> ResponseUpdateUserNameAndLastName:
    try:
        return facade.update_user_name_and_last_name(user_id, data.name, data.last_name)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')


@router.get('/ranks', status_code=status.HTTP_200_OK)
async def get_users_ranking(facade: auth_use_case_dependency, _: token_http_dependency) -> ResponseUsersRanking:
    try:
        return facade.get_users_ranking()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')


@router.get('/ranks/user', status_code=status.HTTP_200_OK)
async def get_user_ranking(facade: auth_use_case_dependency, user_id: token_http_dependency) -> ResponseUserRank:
    try:
        return facade.get_user_ranking(user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')


@router.get('/ranks/category/{rank_id}', status_code=status.HTTP_200_OK)
async def get_users_ranking_by_rank(rank_id: int,
                                    facade: auth_use_case_dependency, _: token_http_dependency) -> ResponseUsersRanking:
    try:
        return facade.get_users_ranking_by_rank(rank_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')


@router.get('/ranks/category/{rank_id}/user', status_code=status.HTTP_200_OK)
async def get_user_ranking_by_rank(rank_id: int, facade: auth_use_case_dependency,
                                   user_id: token_http_dependency) -> ResponseUserRank:
    try:
        return facade.get_user_ranking_by_rank(rank_id=rank_id, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')


@router.post('/test', status_code=status.HTTP_200_OK)
async def test_route_token_session(user_id: token_http_dependency):
    try:
        return user_id
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
