from pydantic import BaseModel

from app.domain.game.entities.player import Player
from app.domain.game.enums.game_state import GameState


class Game(BaseModel):
    game_id: str
    p1: Player
    p2: Player | None = None
    current_player: Player | None = None
    winner_player: Player | None = None
    current_turn: int = 0
    state: GameState
