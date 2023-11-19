from pydantic import BaseModel

from src.domain.player.player import Player


class Game(BaseModel):
    player1: Player
    player2: Player
    _current_player: Player | None = None
    _turn: int = 0

