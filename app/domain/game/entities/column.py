from collections import Counter

from pydantic import BaseModel

from app.domain.game.errors.errors import RemoveValuesFromColumnError, AddValuesFromColumnError


class Column(BaseModel):
    values: list[int] = []
    score: int = 0
    max_length: int = 3

    def is_full(self) -> bool:
        """Validate if the column is full"""
        return len(self.values) >= self.max_length

    def is_empty(self) -> bool:
        """Check if the Column is not empty to remove values on it."""
        return len(self.values) == 0

    def can_remove_values(self, num: int) -> bool:
        return num in self.values

    def add(self, num: int) -> None:
        """Add Die value into column"""
        if self.is_full():
            raise AddValuesFromColumnError("You can't add more values in a full column")
        self.values.append(num)

    def remove(self, num: int) -> list[int]:
        """Add Die value into column"""
        if self.is_empty():
            raise RemoveValuesFromColumnError("Can't remove values from an empty column.")
        removed_indices = []
        for index, value in enumerate(self.values[:]):
            if value == num:
                removed_indices.append(index)
                self.values.remove(value)

        return removed_indices

    def get_remaining_turn(self) -> int:
        """Count how many spaces are empty compare with the max length in the column."""
        return self.max_length - len(self.values)

    def get_score(self) -> int:
        """Calculate the current score point in the column"""
        counter = Counter(self.values)
        # Multiply the repeated values to get the final score
        self.score = sum(val * count * count for val, count in counter.items())
        return self.score
