from pydantic import BaseModel


class ColumnScore(BaseModel):
    val: int = 0

    def get_points(self, column: list[int]) -> int:
        """Sum the current point in the column"""
        # If is an empty list return: 0
        self.val = 0
        if not column:
            return self.val
        current_score: dict[int, int] = {}
        # Add values to the dict
        for die_val in column:
            current_score[die_val] = current_score.get(die_val, 0) + 1
        # Calculate the values point score
        for die_val, counter in current_score.items():
            self.val += (die_val * counter) * counter
        return self.val
