from abc import ABC, abstractmethod
from typing import Annotated, TypeVar

from fastapi import Depends
from pydantic import BaseModel

from app.db.db import db
from app.domain.auth.use_cases.i_auth_use_case import IAuthUseCase
from app.infrastructure.auth.auth_use_case import AuthUseCase
from app.repositories.auth.auth_repository import AuthRepository

T = TypeVar('T')


class Inyectables(BaseModel, ABC):
    @staticmethod
    @abstractmethod
    def get(*args, **kwargs):
        """The user the inyectable function"""


class AuthDependency(Inyectables):
    @staticmethod
    def get() -> AuthRepository:
        return AuthRepository(db=db)


auth_repository_depend = Annotated[AuthRepository, Depends(AuthDependency.get)]


class AuthUseCaseDependency(Inyectables):
    @staticmethod
    def get(repo: auth_repository_depend) -> IAuthUseCase:
        return AuthUseCase(repo=repo)


auth_use_case_depend = Annotated[AuthRepository, Depends(AuthUseCaseDependency.get)]
