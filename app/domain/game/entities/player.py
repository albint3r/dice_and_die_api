from pydantic import BaseModel, field_validator

from app.domain.game.entities.board import Board
from app.domain.game.entities.die import Die
from app.domain.game.errors.errors import InvalidNewBoardInstance, InvalidNewDieInstance


class Player(BaseModel):
    player_id: str
    board: Board
    die: Die

    @field_validator("board")
    def is_new_board(cls, board):
        """Validate is a new [Board] instance."""
        if (isinstance(board, Board) and not board.columns.get(1) and not board.columns.get(2)
                and not board.columns.get(3)):
            return board
        raise InvalidNewBoardInstance("This is not a new Board instance.")

    @field_validator("die")
    def is_new_die(cls, die):
        """Validate is a new [Die] instance."""
        if isinstance(die, Die) and not die.current_number:
            return die
        raise InvalidNewDieInstance("This is not a new Die Instances.")

    def is_player_turn(self, current_player: "Player") -> int:
        """Validate if the user have the current game turn."""
        return self is current_player
