from fastapi import APIRouter, status, Depends, HTTPException

from src.db.db import db
from src.domain.auth.schemas import SchemaSignin, SchemaLogIn, AuthEmailRequest
from src.infrastructure.auth.auth_facade_impl import AuthFacadeImpl
from src.repositories.auth.auth_handler_impl import auth_handler
from src.repositories.auth.auth_repository import AuthRepository

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses={
        status.HTTP_201_CREATED: {"description": "Success Create User"},
        status.HTTP_202_ACCEPTED: {"description": "Email and Password correct"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalide token"},
        status.HTTP_409_CONFLICT: {"description": "Email or Password error."},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"}
    })

facade = AuthFacadeImpl(repo=AuthRepository(db=db))


@router.post('/v1/signin', status_code=status.HTTP_201_CREATED)
def signin_email_and_password(form_data: AuthEmailRequest) -> SchemaSignin:
    # try:
    return facade.signin(form_data.email, form_data.password.get_secret_value(), auth_handler)
    # except Exception as e:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')


@router.post('/v1/login', status_code=status.HTTP_202_ACCEPTED)
def login_email_and_password(form_data: AuthEmailRequest) -> SchemaLogIn:
    try:
        return facade.login(form_data.email, form_data.password.get_secret_value(), auth_handler)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')


@router.post('/v1/login/token', status_code=status.HTTP_202_ACCEPTED)
def login_from_session_token(user_id: str = Depends(auth_handler.auth_wrapper)) -> SchemaLogIn:
    try:
        return facade.login_from_session_token(user_id, auth_handler)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')


@router.post('/v1/test', status_code=status.HTTP_200_OK)
def test_route_token_session(user_id: str = Depends(auth_handler.auth_wrapper)):
    try:
        return user_id
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
