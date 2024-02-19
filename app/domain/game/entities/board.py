from pydantic import BaseModel

from app.domain.game.entities.column import Column

TColumns = dict[int, Column]


class Board(BaseModel):
    columns: TColumns = {1: Column(), 2: Column(), 3: Column()}
    score: int = 0

    def is_full(self) -> bool:
        """Check all the columns are full."""
        return all([column.is_full() for column in self.columns.values()])

    def is_valid_column_index(self, index: int) -> bool:
        """Validate if the selected column index return a Column instance."""
        column = self.columns.get(index)
        return isinstance(column, Column)

    def get_remaining_turn(self) -> int:
        """Count the remaining turns in the board. This calculation considerate all the empty
        spaces to get the final value."""
        return sum(column.get_remaining_turn() for column in self.columns.values())

    def get_score(self) -> int:
        """Calculate the current score point in the board. This calculation considerate all the 3 columns
        and sum there respective scores values."""
        self.score = sum(column.get_score() for column in self.columns.values())
        return self.score
