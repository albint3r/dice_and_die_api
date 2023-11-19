import pytest
from icecream import ic

from src.domain.board.board import Board
from src.domain.die.die import Die


class TestDie:

    @pytest.fixture
    def die(self) -> Die:
        return Die()

    def test_columns_property(self, die):
        """Test the columns property get correctly the columns in the board"""
        board = Board()
        # Check is get empty columns from column 1 to 3.
        col1 = board.get(1)
        col2 = board.get(2)
        col3 = board.get(3)
        expected = type([])
        # First test:
        result = type(col1)
        error_msg = f"Expected value: [{expected}]. Result= {result}"
        assert expected == result, error_msg
        # Second test:
        result = type(col2)
        error_msg = f"Expected value: [{expected}]. Result= {result}"
        assert expected == result, error_msg
        # Third test:
        result = type(col3)
        error_msg = f"Expected value: [{expected}]. Result= {result}"
        assert expected == result, error_msg

    def test_add_column_index(self, die):
        """Test the add method append correctly to the index column indicated"""
        board = Board()
        # Roll the dice
        die.roll()
        expected = die.number
        index = 1
        board.add(index, expected)
        col1 = board.get(index)
        # Check the firs value added in the column
        result = col1[0]
        error_msg = f"Expected value: [{expected}]. Result= {result}"
        assert expected == result, error_msg
