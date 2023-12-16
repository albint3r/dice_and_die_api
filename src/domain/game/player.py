import uuid

from pydantic import BaseModel, field_validator, validate_call, Field
from starlette.websockets import WebSocket

from src.domain.auth.user import User
from src.domain.game.board import Board
from src.domain.game.die import Die
from src.domain.game.errors import InvalidNewBoard, InvalidNewDie


class Player(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user: User | None = None
    board: Board
    die: Die

    @property
    def die_result(self) -> int:
        return self.die.number

    @field_validator("board")
    def is_new_board(cls, boar):
        if isinstance(boar, Board) and not boar.col1 and not boar.col2 and not boar.col3:
            return boar
        raise InvalidNewBoard(
            f'This is a invalid new board. Check if type: [Board] and have empty columns:'
            f' col1: {boar.col1}, col2: {boar.col2}, col3: {boar.col3}')

    @field_validator("die")
    def is_new_die(cls, die):
        if isinstance(die, Die) and not die.number:
            return die
        raise InvalidNewDie(f'This is not a new Die. It have {die.number}')

    @validate_call()
    def roll_dice(self) -> None:
        """Player roll their dice"""
        self.die.roll()

    @validate_call()
    def add_dice_in_board_col(self, col_index: int, value: int) -> None:
        """Player add the dice value in the board"""
        self.board.add(col_index, value)

    @validate_call()
    def can_add_to_board_col(self, col_index: int) -> bool:
        """Check if the Player can add to the board column"""
        return self.board.cad_add(col_index)

    @validate_call()
    def remove_dices_in_board_col(self, col_index: int, value: int) -> None:
        """Remove all the values in the player board column index"""
        self.board.remove(col_index, value)

    @validate_call()
    def is_same_player(self, other) -> bool:
        """Check if the player is the same"""
        return self is other

    @validate_call()
    def update_points(self, col_index: int) -> None:
        """Get the points and update in the same process"""
        self.board.update_score(col_index)

    def update_total_score(self) -> None:
        self.board.update_total_score()
