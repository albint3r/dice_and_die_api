from pydantic import BaseModel
from fastapi import status
from app.domain.core.ref_types import TActiveGames
from app.domain.lobby.entities.lobby import Lobby


class ResponseActiveGames(BaseModel):
    response: TActiveGames
    status_code: int = status.HTTP_200_OK


class ResponseTotalConnectedUsers(BaseModel):
    total: int
    status_code: int = status.HTTP_200_OK


class ResponseLobbyInformation(BaseModel):
    lobby: Lobby
    total_players: int
