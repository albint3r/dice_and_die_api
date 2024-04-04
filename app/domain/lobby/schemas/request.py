from pydantic import BaseModel

from app.domain.lobby.enums.lobby_events import LobbyEvents


class LobbyEventRequest(BaseModel):
    event: LobbyEvents
