from pydantic import BaseModel

from app.domain.game.enums.game_event import GameEvent


class GamePlayerRequest(BaseModel):
    """This is the Base Game Request"""
    event: GameEvent
