import pytest

from src.domain.board.board import Board
from src.domain.die.die import Die
from src.domain.player.errors import InvalidNewBoard, InvalidNewDie
from src.domain.player.player import Player


class TestPlayer:
    """Test the player Class entity"""

    @pytest.fixture
    def die(self):
        return Die()

    @pytest.fixture
    def board(self):
        return Board()

    def test_invalid_new_board(self):
        """Test invalid new board. Expected an empty board columns"""
        die = Die()
        board = Board()
        board.add(1, 1)
        with pytest.raises(InvalidNewBoard):
            _ = Player(die=die, board=board)

    def test_invalid_new_die(self):
        """Test invalid new die. Expected a None number die value"""
        die = Die()
        die.roll()
        board = Board()
        with pytest.raises(InvalidNewDie):
            _ = Player(die=die, board=board)

    def test_valid_new_player(self, board, die):
        """Test correct player creations"""
        expected = "Player()"
        result = Player(board=board, die=die)
        error_msg = f'Expected value: {expected}. Result: {result}'
        assert isinstance(result, Player), error_msg
