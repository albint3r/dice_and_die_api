from src.domain.game.schemes import ActiveGamesResponses
from src.domain.waiting_room.i_waiting_room_facade import IWaitingRoomFacade
from src.infrastructure.core.websocket_manager_impl import _WsManagerImpl


class WaitingRoomFacadeImpl(IWaitingRoomFacade):
    def getActiveResponses(self, ws_manager: _WsManagerImpl) -> ActiveGamesResponses:
        active_games = ws_manager.active_games
        return ActiveGamesResponses(response=active_games)
