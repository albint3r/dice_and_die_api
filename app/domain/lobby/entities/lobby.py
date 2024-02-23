from pydantic import BaseModel

from app.domain.core.ref_types import TActiveGames


class Lobby(BaseModel):
    active_games: TActiveGames
