from random import randint

from pydantic import BaseModel


class Die(BaseModel):
    current_number: int | None = None
    _min_head: int = 1
    _max_head: int = 6

    def roll(self) -> None:
        """Roll the dice to get a current number"""
        self.current_number = randint(self._min_head, self._max_head)
