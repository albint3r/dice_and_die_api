from pydantic import BaseModel

from app.domain.game.enums.game_event import GameEvent
from app.domain.game.enums.viewer_event import ViewerEvent


class GamePlayerRequest(BaseModel):
    """This is the Game Request"""
    event: GameEvent


class ViewerRequest(BaseModel):
    """This Viewer Request"""
    event: ViewerEvent
