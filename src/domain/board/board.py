from pydantic import BaseModel, validate_call


class Board(BaseModel):
    """This represents the board of each player. This is a 3x3 grid board"""
    col1: list[int] = []
    col2: list[int] = []
    col3: list[int] = []
    _max: int = 3
    _min: int = 0

    @property
    def columns(self) -> dict[int, list[int]]:
        return {1: self.col1, 2: self.col2, 3: self.col3}

    @property
    def is_full(self) -> bool:
        """Return True if the board columns are full"""
        col1 = len(self.get(1))
        col2 = len(self.get(2))
        col3 = len(self.get(3))
        _max = self._max
        return col1 == _max and col2 == _max and col3 == _max

    @validate_call()
    def get(self, col_index: int) -> list[int]:
        return self.columns.get(col_index)

    @validate_call()
    def add(self, col_index: int, value: int) -> None:
        """Add the dice value in the column index"""
        if self.is_valid_index(col_index) and self.cad_add(col_index):
            column = self.columns.get(col_index)
            column.append(value)

    @validate_call()
    def remove(self, col_index: int, value: int) -> None:
        """Remove all the values in the column"""
        if self.is_valid_index(col_index) and self.cad_remove(col_index):
            column = self.columns.get(col_index)
            while value in column:
                column.remove(value)

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
