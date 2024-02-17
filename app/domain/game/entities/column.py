from collections import Counter
from pydantic import BaseModel

from app.domain.core.ref_types import TCurrentScore
from app.domain.game.errors.errors import RemoveValuesFromColumnError, AddValuesFromColumnError


class Column(BaseModel):
    values: list[int] = []
    score: int = 0
    _max_length: int = 3

    def is_full(self) -> bool:
        """Validate if the column is full"""
        return len(self.values) >= self._max_length

    def is_empty(self) -> bool:
        """Check if the Column is not empty to remove values on it."""
        return len(self.values) == 0

    def add(self, num: int) -> None:
        """Add Die value into column"""
        if self.is_full():
            raise AddValuesFromColumnError("You can't add more values in a full column")
        self.values.append(num)

    def remove(self, num: int) -> None:
        """Add Die value into column"""
        if self.is_empty():
            raise RemoveValuesFromColumnError("Can't remove values from an empty column.")
        while num in self.values:
            self.values.remove(num)

    def get_remaining_turn(self) -> int:
        """Count how many spaces are empty compare with the max length in the column."""
        return self._max_length - len(self.values)

    def get_score(self) -> int:
        """Calculate the current score point in the column"""
        counter: TCurrentScore = Counter(self.values)
        # Multiply the repeated values to get the final score
        self.score = sum(val * count * count for val, count in counter.items())
        return self.score
