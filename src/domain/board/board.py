from icecream import ic
from pydantic import BaseModel, validate_call


class Board(BaseModel):
    """This represents the board of each player. This is a 3x3 grid board"""
    col1: list[int] = []
    col2: list[int] = []
    col3: list[int] = []
    _max: int = 3

    @property
    def columns(self) -> dict[int, list[int]]:
        return {1: self.col1, 2: self.col2, 3: self.col3}

    @validate_call()
    def get(self, col_index: int) -> list[int]:
        return self.columns.get(col_index)

    @validate_call()
    def add(self, col_index: int, value: int) -> None:
        """Add the dice value in the column index"""
        if 0 < col_index < 4 and self.cad_add(col_index):
            ic()
            column = self.columns.get(col_index)
            column.append(value)

    @validate_call()
    def cad_add(self, col_index: int) -> bool:
        """Check if is possible to add a value to the column index.
        The max length of values you can add to each column is 3."""
        column = self.columns.get(col_index)
        return len(column) < self._max
