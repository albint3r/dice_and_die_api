from pydantic import BaseModel, validate_call

from src.domain.game.player import Player


class Game(BaseModel):
    p1: Player
    p2: Player
    _current_player: Player | None = None
    _turn: int = 0

    @property
    def current_player(self) -> Player:
        return self._current_player

    @property
    def is_finish(self) -> bool:
        """Validate if the game is finished"""
        return self.p1.board.is_full or self.p2.board.is_full

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

    @validate_call()
    def can_destroy_opponent_target_column(self, col_index: int, value: int) -> bool:
        """Check if the user have values in the target column"""
        opponent_player = self.get_inverse_player()
        target_column = opponent_player.board.get(col_index)
        return value in target_column

    @validate_call()
    def destroy_opponent_target_column(self, col_index: int, value: int) -> None:
        """Remove all the values in the target column"""
        opponent_player = self.get_inverse_player()
        opponent_player.remove_dices_in_board_col(col_index, value)
