from pydantic import BaseModel, validate_call, Field

from src.domain.game.column_score import ColumScore
from src.domain.game.errors import AddError, InvalidColumnError, RemoveError


class Board(BaseModel):
    """This represents the board of each player. This is a 3x3 grid board"""
    col1: list[int] = []
    col2: list[int] = []
    col3: list[int] = []
    score1: ColumScore = Field(default_factory=ColumScore)
    score2: ColumScore = Field(default_factory=ColumScore)
    score3: ColumScore = Field(default_factory=ColumScore)
    total_score: int = 0
    _max: int = 3
    _min: int = 0

    @property
    def columns(self) -> dict[int, list[int]]:
        """This is a dict of the columns index"""
        return {1: self.col1, 2: self.col2, 3: self.col3}

    @property
    def columns_score(self) -> dict[int, ColumScore]:
        """This is a dict of the columns scores index"""
        return {1: self.score1, 2: self.score2, 3: self.score3}

    @property
    def is_full(self) -> bool:
        """Return True if the board columns are full"""
        col1 = len(self.get_column(1))
        col2 = len(self.get_column(2))
        col3 = len(self.get_column(3))
        _max = self._max
        return col1 == _max and col2 == _max and col3 == _max

    @validate_call()
    def get_column(self, col_index: int) -> list[int]:
        """Get the column index attribute of the board"""
        col = self.columns.get(col_index)
        if isinstance(col, list):
            return col
        raise InvalidColumnError(f'This is a invalid column index: {col_index}')

    @validate_call()
    def update_score(self, col_index: int) -> ColumScore:
        """Get the column index attribute of the board"""
        column = self.columns.get(col_index)
        score = self.columns_score.get(col_index)
        if isinstance(column, list) and isinstance(score, ColumScore):
            _ = score.get_points(column=column)
            return score
        raise InvalidColumnError(f'This is a invalid column index: {col_index}')

    def update_total_score(self) -> None:
        self.total_score = self.score1.val + self.score2.val + self.score3.val

    @validate_call()
    def add(self, col_index: int, value: int) -> None:
        """Add the dice value in the column index"""
        if self.is_valid_index(col_index) and self.cad_add(col_index):
            column = self.columns.get(col_index)
            column.append(value)
            return None
        raise AddError(f"You can't add more values in the Board Column: {col_index}")

    @validate_call()
    def remove(self, col_index: int, value: int) -> None:
        """Remove all the values in the column"""
        if self.is_valid_index(col_index) and self.cad_remove(col_index):
            column = self.columns.get(col_index)
            while value in column:
                column.remove(value)
            return None
        raise RemoveError(f"You can't remove more values in the Board Column: {col_index}")

    @validate_call()
    def cad_add(self, col_index: int) -> bool:
        """Check if is possible to add a value to the column index.
        The max length of values you can add to each column is 3."""
        column = self.columns.get(col_index)
        return len(column) < self._max

    @validate_call()
    def cad_remove(self, col_index: int) -> bool:
        """Check if is possible to remove all the values the column. """
        column = self.columns.get(col_index)
        return len(column) > self._min

    @validate_call()
    def is_valid_index(self, col_index: int) -> bool:
        """Validate the index is between 0 and 4. Valid values [1,2,3]"""
        return 0 < col_index < 4
