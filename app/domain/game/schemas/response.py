from pydantic import BaseModel

from app.domain.core.ref_types import TExtras
from app.domain.game.entities.game import Game


class GameResponse(BaseModel):
    """This is the Base Game Response"""
    game: Game
    extras: TExtras
    message: str
