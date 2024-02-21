from pydantic import BaseModel

from app.domain.core.ref_types import TExtras
from app.domain.game.enums.game_event import GameEvent
from app.domain.game.enums.viewer_event import ViewerEvent


class GamePlayerRequest(BaseModel):
    """This is the Game Request"""
    event: GameEvent
    extras: TExtras = {}


class ViewerRequest(BaseModel):
    """This Viewer Request"""
    event: ViewerEvent
