from app.domain.lobby.schemas.response import ResponseTotalConnectedUsers, ResponseActiveGames
from app.domain.lobby.use_cases.i_lobby_use_case import ILobbyUseCase


class LobbyUseCase(ILobbyUseCase):
    def get_active_games(self) -> ResponseActiveGames:
        pass

    def get_total_connected_users(self) -> ResponseTotalConnectedUsers:
        pass
