import pytest
from fastapi.testclient import TestClient
from icecream import ic

from app.domain.game.entities.die import Die
from app.main import app


class TestGame:
    """Testing the game components"""

    @pytest.fixture
    def die(self) -> Die:
        return Die()

    def test_dice_start_with_null_value(self, die):
        """Test the dice allways start with null current value."""
        expected = None
        # Start test
        result = die.current_number
        erros_msg = f'Expected {expected}. And You get {result}'
        assert result is expected, erros_msg

    def test_dice_roll_between_one_and_six(self, die):
        """This test the dice numbers are between the 1 and six"""
        max_num = 6
        min_num = 1
        # Start test
        die.roll()
        result = die.current_number
        erros_msg = f'Expected a number between {max_num} and {min_num}. And You get {result}'
        assert min_num <= result <= max_num, erros_msg

    def test_player_create_new_game(self):
        client = TestClient(app)
        FAKE_GAME_ID = 'FAKE_GAME_ID'
        with client.websocket_connect(f"/v2/game/{FAKE_GAME_ID}/'tobe") as websocket:
            data = websocket.receive_json()
            # assert data == {"msg": "Hello WebSocket"}
            assert False
