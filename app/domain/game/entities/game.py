from datetime import datetime

from pydantic import BaseModel, Field

from app.domain.game.entities.game_config import GameConfig
from app.domain.game.entities.player import Player
from app.domain.game.enums.game_state import GameState

TWinner = tuple[Player, Player | None]


class Game(BaseModel):
    create_date: datetime = Field(default_factory=datetime.now)
    game_id: str
    p1: Player
    p2: Player | None = None
    current_player: Player | None = None
    winner_player: TWinner | None = None
    current_turn: int = 0
    state: GameState
    config: GameConfig | None = None

    @property
    def is_finished(self) -> bool:
        """Validate if the game is finished"""
        # Without Player two this function have None Type erro. Because that return False.
        if self.p2:
            return self.p1.board.is_full() or self.p2.board.is_full()
        return False

    @property
    def is_waiting_opponent(self) -> bool:
        """Validate if the player 1 is waiting opponent"""
        return self.state == GameState.WAITING_OPPONENT

    def get_opponent_player(self) -> Player:
        return self.p1 if self.current_player == self.p2 else self.p2

    def get_winner(self) -> TWinner:
        """Get the winner of the game. If the game was a draw return both player"""
        if self.p1.board.score > self.p2.board.score:
            self.winner_player = (self.p1, None)
        elif self.p2.board.score > self.p1.board.score:
            self.winner_player = (self.p2, None)
        else:
            self.winner_player = (self.p1, self.p2)
        return self.winner_player
