import pytest

from src.domain.game.die import Die


class TestDie:

    @pytest.fixture
    def die(self) -> Die:
        return Die()

    def test_die_roll_min_max(self, die):
        """Validate the dice roll between 1 an 6"""
        max_val = 6
        min_val = 1
        die.roll()
        result = die.number
        error_msg = f"Expected values: max:{max_val} and min: {min_val}. Result= {result}"
        assert min_val <= result <= max_val, error_msg
