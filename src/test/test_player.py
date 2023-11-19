import pytest

from src.domain.board.board import Board
from src.domain.die.die import Die


class TestPlayer:
    """Test the player Class entity"""

    @pytest.fixture
    def die(self):
        return Die()

    @pytest.fixture
    def board(self):
        return Board()

    # def test_

