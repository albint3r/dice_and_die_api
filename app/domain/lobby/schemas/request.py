from pydantic import BaseModel

from app.domain.lobby.enums.lobby_events import LobbyEvents


class RequestLobbyEvent(BaseModel):
    event: LobbyEvents
