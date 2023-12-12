from fastapi import APIRouter, status, Depends

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
def email_and_password_signin(form_data: AuthEmailRequest) -> SchemaSignin:
    return facade.signin(form_data.email, form_data.password.get_secret_value(), auth_handler)


@router.post('/v1/login', status_code=status.HTTP_202_ACCEPTED)
def email_and_password_login(form_data: AuthEmailRequest) -> SchemaLogIn:
    return facade.login(form_data.email, form_data.password.get_secret_value(), auth_handler)


@router.post('/v1/test', status_code=status.HTTP_200_OK)
def email_and_password_login(user_id: str = Depends(auth_handler.auth_wrapper)):
    return user_id
