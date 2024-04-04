from abc import ABC, abstractmethod
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel

from app.db.db import db
from app.domain.analytics.use_cases.i_analytics_use_case import IAnalyticsUseCase
from app.domain.auth.use_cases.i_auth_use_case import IAuthUseCase
from app.domain.game.entities.game_config import GameConfig
from app.domain.game.enums.game_mode import GameMode
from app.domain.game.use_cases.i_chat_observer import IChatObserver
from app.domain.game.use_cases.i_game_use_case import IGameUseCase
from app.domain.game.use_cases.i_game_websocket_manager import IGameWebSocketManager
from app.domain.game.use_cases.i_games_mode_runner import IGamesModeRunner
from app.domain.game.use_cases.i_progress_use_case import ILevelUseCase, IRankUseCase
from app.domain.game.use_cases.i_user_level_use_case import IManagerLevelingUseCase
from app.domain.game.use_cases.i_view_use_case import IViewUseCase
from app.domain.game.use_cases.i_viewers_websocket_manager import IViewersWebSocketManager
from app.domain.lobby.use_cases.i_lobby_use_case import ILobbyUseCase
from app.domain.lobby.use_cases.i_lobby_websocket_manager import ILobbyWebSocketManager
from app.infrastructure.analytics.analytics_use_case import AnalyticsUseCase
from app.infrastructure.auth.auth_use_case import AuthUseCase
from app.infrastructure.game.adventure_game_mode_runner import AdventureGameModeRunner
from app.infrastructure.game.chat_observer import ChatObserver
from app.infrastructure.game.game_use_case import GameUseCase
from app.infrastructure.game.game_websocket_manager import game_websocket_manger
from app.infrastructure.game.level_use_case import LevelUserCase
from app.infrastructure.game.manager_leveling_use_case import ManagerLevelingUseCase
from app.infrastructure.game.pve_game_use_case import PVEGameUseCase
from app.infrastructure.game.rank_use_case import RankUseCase
from app.infrastructure.game.view_user_cases import ViewUseCase
from app.infrastructure.game.viewers_websocket_manager import viewers_websocket_manager
from app.infrastructure.lobby.lobby_use_case import LobbyUseCase
from app.infrastructure.lobby.lobby_websocket_manager import lobby_websocket_manager
from app.repositories.analytics.analytics_repository import AnalyticsRepository
from app.repositories.auth.auth_repository import AuthRepository


class Inyectables(BaseModel, ABC):

    @staticmethod
    @abstractmethod
    def inject(*args, **kwargs):
        """The user the inyectable function"""


class AuthRepositoryDependency(Inyectables):
    @staticmethod
    def inject() -> AuthRepository:
        return AuthRepository(db=db)


auth_repository_dependency = Annotated[AuthRepository, Depends(AuthRepositoryDependency.inject)]


class AnalyticsRepositoryDependency(Inyectables):
    @staticmethod
    def inject() -> AnalyticsRepository:
        return AnalyticsRepository(db=db)


analytics_repository_dependency = Annotated[AnalyticsRepository, Depends(AnalyticsRepositoryDependency.inject)]


class AuthUseCaseDependency(Inyectables):
    @staticmethod
    def inject(repo: auth_repository_dependency) -> IAuthUseCase:
        return AuthUseCase(repo=repo)


auth_use_case_dependency = Annotated[IAuthUseCase, Depends(AuthUseCaseDependency.inject)]


class AnalyticUseCaseDependency(Inyectables):

    @staticmethod
    def inject(repo: analytics_repository_dependency) -> IAnalyticsUseCase:
        return AnalyticsUseCase(repo=repo)


analytics_use_case_dependency = Annotated[IAnalyticsUseCase, Depends(AnalyticUseCaseDependency.inject)]


class LobbyWebSocketDependency(Inyectables):

    @staticmethod
    def inject() -> ILobbyWebSocketManager:
        return lobby_websocket_manager


lobby_websocket_dependency = Annotated[ILobbyWebSocketManager, Depends(LobbyWebSocketDependency.inject)]


class LobbyUseCaseDependency(Inyectables):

    @staticmethod
    def inject() -> ILobbyUseCase:
        return LobbyUseCase(lobby_websocket_manager=lobby_websocket_manager,
                            game_websocket_manager=game_websocket_manger)


lobby_use_case_dependency = Annotated[ILobbyUseCase, Depends(LobbyUseCaseDependency.inject)]


class LevelUseCaseDependency(Inyectables):

    @staticmethod
    def inject() -> ILevelUseCase:
        return LevelUserCase()


level_use_case_dependency = Annotated[ILevelUseCase, Depends(LevelUseCaseDependency.inject)]


class RankUseCaseDependency(Inyectables):

    @staticmethod
    def inject() -> IRankUseCase:
        return RankUseCase()


rank_use_case_dependency = Annotated[IRankUseCase, Depends(RankUseCaseDependency.inject)]


class ManagerLevelingUseCaseDependency(Inyectables):

    @staticmethod
    def inject(level_manager: level_use_case_dependency,
               rank_manager: rank_use_case_dependency) -> IManagerLevelingUseCase:
        return ManagerLevelingUseCase(leve_manager=level_manager, rank_manager=rank_manager)


manager_leveling_use_case_dependency = Annotated[
    IManagerLevelingUseCase, Depends(ManagerLevelingUseCaseDependency.inject)]


class GameWebSocketDependency(Inyectables):

    @staticmethod
    def inject() -> IGameWebSocketManager:
        return game_websocket_manger


game_websocket_dependency = Annotated[IGameWebSocketManager, Depends(GameWebSocketDependency.inject)]


class ViewersWebSocketDependency(Inyectables):

    @staticmethod
    def inject() -> IViewersWebSocketManager:
        return viewers_websocket_manager


viewers_websocket_dependency = Annotated[IViewersWebSocketManager, Depends(ViewersWebSocketDependency.inject)]


class PVPGameUseCaseDependency(Inyectables):
    @staticmethod
    def inject(game_websocket: game_websocket_dependency,
               view_websocket: viewers_websocket_dependency,
               leveling_manager: manager_leveling_use_case_dependency,
               repo: auth_repository_dependency) -> IGameUseCase:
        leveling_manager._base_win_points = 0

        return PVEGameUseCase(websocket_manager=game_websocket,
                              viewers_websocket_manager=view_websocket,
                              leveling_manager=leveling_manager,
                              repo=repo)


pve_game_use_case_dependency = Annotated[IGameUseCase, Depends(PVPGameUseCaseDependency.inject)]


class GameUseCaseDependency(Inyectables):
    @staticmethod
    def inject(game_websocket: game_websocket_dependency,
               view_websocket: viewers_websocket_dependency,
               leveling_manager: manager_leveling_use_case_dependency,
               repo: auth_repository_dependency) -> IGameUseCase:
        return GameUseCase(websocket_manager=game_websocket,
                           viewers_websocket_manager=view_websocket,
                           leveling_manager=leveling_manager,
                           repo=repo)


game_use_case_dependency = Annotated[IGameUseCase, Depends(GameUseCaseDependency.inject)]


class ViewersUseCaseDependency(Inyectables):
    @staticmethod
    def inject(game_websocket: game_websocket_dependency,
               view_websocket: viewers_websocket_dependency,
               repo: auth_repository_dependency) -> IViewUseCase:
        return ViewUseCase(websocket_manager=game_websocket,
                           viewers_websocket_manager=view_websocket,
                           repo=repo)


viewers_use_case_dependency = Annotated[IViewUseCase, Depends(ViewersUseCaseDependency.inject)]


class ChatObserverDependency(Inyectables):
    @staticmethod
    def inject(game_websocket: game_websocket_dependency,
               view_websocket: viewers_websocket_dependency) -> IChatObserver:
        return ChatObserver(websockets_manager=game_websocket,
                            viewers_websockets_manager=view_websocket)


chat_observer_dependency = Annotated[IChatObserver, Depends(ChatObserverDependency.inject)]


class AdventureGameModeRunnerDependency(Inyectables):
    @staticmethod
    def inject(ws_game: game_websocket_dependency, repo: auth_repository_dependency) -> IGamesModeRunner:
        return AdventureGameModeRunner(config=GameConfig(mode=GameMode.ADVENTURE),
                                       ws_game=ws_game,
                                       repo=repo)


adventure_game_mode_runner_dependency = Annotated[IGamesModeRunner, Depends(AdventureGameModeRunnerDependency.inject)]
