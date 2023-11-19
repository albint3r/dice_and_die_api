from pydantic import BaseModel, validate_call

from src.domain.player.player import Player


class Game(BaseModel):
    p1: Player
    p2: Player
    _current_player: Player | None = None
    _turn: int = 0

    @validate_call()
    def set_current_player(self, player: Player) -> None:
        """Set the current player turn"""
        self._current_player = player

    def add_turn(self) -> None:
        """Add plus +1 to the turn value"""
        self._turn += 1

    def get_inverse_player(self) -> Player | None:
        """Get the inverse player of the current player"""
        if self._current_player is not None:
            # Devuelve p1 si el jugador actual es p2 y viceversa
            return self.p1 if self._current_player == self.p2 else self.p2
        return None
