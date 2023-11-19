from random import randint

from pydantic import BaseModel


class Die(BaseModel):
    """The dice that players roll each turn"""
    number: int | None = None
    _min: int = 1
    _max: int = 6

    def roll(self) -> None:
        """Roll the dice a return an integer with a value between 1 an 6"""
        self.number = randint(self._min, self._max)
