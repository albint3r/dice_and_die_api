from abc import ABC, abstractmethod
from typing import Annotated, TypeVar

from fastapi import Depends
from pydantic import BaseModel

from app.db.db import db
from app.domain.analytics.use_cases.i_analytics_use_case import IAnalyticsUseCase
from app.domain.auth.use_cases.i_auth_use_case import IAuthUseCase
from app.domain.lobby.use_cases.i_lobby_use_case import ILobbyUseCase
from app.domain.lobby.use_cases.i_lobby_websocket_manager import ILobbyWebSocketManager
from app.infrastructure.analytics.analytics_use_case import AnalyticsUseCase
from app.infrastructure.auth.auth_use_case import AuthUseCase
from app.infrastructure.game.game_websocket_manager import game_websocket_manger
from app.infrastructure.lobby.lobby_use_case import LobbyUseCase
from app.infrastructure.lobby.lobby_websocket_manager import lobby_websocket_manager
from app.repositories.analytics.analytics_repository import AnalyticsRepository
from app.repositories.auth.auth_repository import AuthRepository


class Inyectables(ABC):
    @staticmethod
    @abstractmethod
    def inject(*args, **kwargs):
        """The user the inyectable function"""


class AuthRepositoryDependency(Inyectables):
    @staticmethod
    def inject() -> AuthRepository:
        return AuthRepository(db=db)


auth_repository_depend = Annotated[AuthRepository, Depends(AuthRepositoryDependency.inject)]


class AnalyticsRepositoryDependency(Inyectables):
    @staticmethod
    def inject() -> AnalyticsRepository:
        return AnalyticsRepository(db=db)


analytics_repository_depend = Annotated[AnalyticsRepository, Depends(AnalyticsRepositoryDependency.inject)]


class AuthUseCaseDependency(Inyectables):
    @staticmethod
    def inject(repo: auth_repository_depend) -> IAuthUseCase:
        return AuthUseCase(repo=repo)


auth_use_case_depend = Annotated[IAuthUseCase, Depends(AuthUseCaseDependency.inject)]


class AnalyticUseCaseDependency(Inyectables):

    @staticmethod
    def inject(repo: analytics_repository_depend) -> IAnalyticsUseCase:
        return AnalyticsUseCase(repo=repo)


analytics_use_case_depend = Annotated[IAnalyticsUseCase, Depends(AnalyticUseCaseDependency.inject)]


class LobbyWebSocketDependency(Inyectables):

    @staticmethod
    def inject(*args, **kwargs) -> ILobbyWebSocketManager:
        return lobby_websocket_manager


lobby_websocket_dependency = Annotated[ILobbyWebSocketManager, Depends(LobbyWebSocketDependency.inject)]


class LobbyUseCaseDependency(Inyectables):

    @staticmethod
    def inject(*args, **kwargs) -> ILobbyUseCase:
        return LobbyUseCase(lobby_websocket_manager=lobby_websocket_manager,
                            game_websocket_manager=game_websocket_manger)


lobby_use_case_dependency = Annotated[ILobbyUseCase, Depends(LobbyUseCaseDependency.inject)]
