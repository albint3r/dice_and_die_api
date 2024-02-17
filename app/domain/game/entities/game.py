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

    @property
    def is_finished(self) -> bool:
        """Validate if the game is finished"""
        return self.p1.board.is_full() or self.p2.board.is_full()

    @property
    def is_waiting_opponent(self) -> bool:
        """Validate if the player 1 is waiting opponent"""
        return self.state == GameState.WAITING_OPPONENT
