from pydantic import BaseModel, validate_call, Field

from src.domain.game.player import Player


class Game(BaseModel):
    id: str | None = None
    p1: Player | None = None
    p2: Player | None = None
    current_player: Player | None = None
    turn: int = 0

    @property
    def is_finish(self) -> bool:
        """Validate if the game is finished"""
        return self.p1.board.is_full or self.p2.board.is_full

    @property
    def is_waiting_player(self) -> bool:
        """Validate if the game is finished"""
        return self.p1 is None or self.p2 is None

    def is_player_turn(self, player: Player) -> bool:
        """Return True if is the players current turn"""
        return player is self.current_player

    @validate_call()
    def set_current_player(self, player: Player) -> None:
        """Set the current player turn"""
        self.current_player = player

    def add_turn(self) -> None:
        """Add plus +1 to the turn value"""
        self.turn += 1

    def get_inverse_player(self) -> Player | None:
        """Get the inverse player of the current player"""
        if self.current_player is not None:
            # Devuelve p1 si el jugador actual es p2 y viceversa
            return self.p1 if self.current_player == self.p2 else self.p2
        return None

    @validate_call()
    def can_destroy_opponent_target_column(self, col_index: int, value: int) -> bool:
        """Check if the user have values in the target column"""
        opponent_player = self.get_inverse_player()
        target_column = opponent_player.board.get_column(col_index)
        return value in target_column

    @validate_call()
    def destroy_opponent_target_column(self, col_index: int, value: int) -> None:
        """Remove all the values in the target column"""
        opponent_player = self.get_inverse_player()
        opponent_player.remove_dices_in_board_col(col_index, value)

    @validate_call()
    def update_players_points(self, col_index: int) -> None:
        """Update single ant total score of the players"""
        # Update Player 1
        self.p1.update_points(col_index)
        self.p1.update_total_score()
        # Update Player 2
        self.p2.update_points(col_index)
        self.p2.update_total_score()
