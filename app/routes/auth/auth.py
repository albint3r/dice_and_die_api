from fastapi import APIRouter, status, Depends, HTTPException

from app.db.db import db
from app.domain.auth.schemas.request import RequestAuthEmail
from app.domain.auth.schemas.response import ResponseLogIn, ResponseSignin
from app.infrastructure.auth.auth_handler_impl import auth_handler
from app.infrastructure.auth.auth_use_case import AuthUseCase
from app.repositories.auth.auth_repository import AuthRepository

router = APIRouter(
    prefix='/auth/v1',
    tags=['auth'],
    responses={
        status.HTTP_201_CREATED: {"description": "Success Create User"},
        status.HTTP_202_ACCEPTED: {"description": "Email and Password correct"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalide token"},
        status.HTTP_409_CONFLICT: {"description": "Email or Password error."},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"}
    })


@router.post('/signin', status_code=status.HTTP_201_CREATED)
def signin_email_and_password(form_data: RequestAuthEmail) -> ResponseSignin:
    # try:
    facade = AuthUseCase(repo=AuthRepository(db=db))
    return facade.signin(form_data.email, form_data.password.get_secret_value(), auth_handler)
    # except Exception as e:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')


@router.post('/login', status_code=status.HTTP_202_ACCEPTED)
def login_email_and_password(form_data: RequestAuthEmail) -> ResponseLogIn:
    try:
        facade = AuthUseCase(repo=AuthRepository(db=db))
        return facade.login(form_data.email, form_data.password.get_secret_value(), auth_handler)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')


@router.post('/login/token', status_code=status.HTTP_202_ACCEPTED)
def login_from_session_token(user_id: str = Depends(auth_handler.auth_wrapper)) -> ResponseLogIn:
    try:
        facade = AuthUseCase(repo=AuthRepository(db=db))
        return facade.login_from_session_token(user_id, auth_handler)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')


@router.post('/test', status_code=status.HTTP_200_OK)
def test_route_token_session(user_id: str = Depends(auth_handler.auth_wrapper)):
    try:
        return user_id
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
