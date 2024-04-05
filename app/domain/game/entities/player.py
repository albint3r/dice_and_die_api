import uuid

from pydantic import BaseModel, field_validator, Field

from app.domain.auth.entities.user import User
from app.domain.game.entities.board import Board
from app.domain.game.entities.column import Column
from app.domain.game.entities.die import Die
from app.domain.game.entities.player_rol import PlayerRol
from app.domain.game.errors.errors import InvalidNewBoardInstance, InvalidNewDieInstance


class Player(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user: User
    board: Board
    die: Die
    rol: PlayerRol = PlayerRol.HUMAN

    @field_validator("board")
    def is_new_board(cls, board):
        """Validate is a new [Board] instance."""
        if isinstance(board, Board) and not board.columns.get(1).values:
            return board
        raise InvalidNewBoardInstance("This is not a new Board instance.")

    @field_validator("die")
    def is_new_die(cls, die):
        """Validate is a new [Die] instance."""
        if isinstance(die, Die) and not die.current_number:
            return die
        raise InvalidNewDieInstance("This is not a new Die Instances.")

    def is_player_turn(self, player: "Player") -> int:
        """Validate if the user have the current game turn."""
        return self is player

    def reset_board(self, col_length: int, total_columns: int) -> None:
        """Reset the board and die of the game"""
        self.board = Board(columns={i: Column(max_length=col_length) for i in range(1, total_columns + 1)})
        self.die.current_number = None
