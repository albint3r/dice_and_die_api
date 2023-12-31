import pytest

from src.domain.game.board import Board
from src.domain.game.die import Die
from src.domain.game.errors import InvalidColumnError, AddError, RemoveError


class TestBoar:

    @pytest.fixture
    def die(self) -> Die:
        return Die()

    def test_columns_property(self, die):
        """Test the columns property get correctly the columns in the board"""
        board = Board()
        # Check is get empty columns from column 1 to 3.
        col1 = board.get_column(1)
        col2 = board.get_column(2)
        col3 = board.get_column(3)
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
        col1 = board.get_column(index)
        # Check the firs value added in the column
        result = col1[0]
        error_msg = f"Expected value: [{expected}]. Result= {result}"
        assert expected == result, error_msg

    def test_can_add_more(self, die):
        """Test the player cand add more items"""
        board = Board()
        # Roll the dice
        die.roll()
        expected = True
        index = 1
        board.add(index, die.number)
        # Check the firs value added in the column
        result = board.cad_add(index)
        error_msg = f"Expected value: [{expected}]. Result= {result}"
        assert expected is result, error_msg

    def test_can_not_add_more(self, die):
        """Test the player can not add more values in the column"""
        board = Board()
        # Roll the dice
        die.roll()
        expected = False
        index = 1
        board.add(index, die.number)
        board.add(index, die.number)
        board.add(index, die.number)
        # Check the firs value added in the column
        result = board.cad_add(index)
        error_msg = f"Expected value: [{expected}]. Result= {result}"
        assert expected is result, error_msg

    def test_can_not_remove(self, die):
        """Test the method remove return false, because is empty"""
        board = Board()
        # Roll the dice
        die.roll()
        expected = False
        index = 1
        result = board.cad_remove(index)
        error_msg = f"Expected value: [{expected}]. Result= {result}"
        assert expected is result, error_msg

    def test_can_remove(self, die):
        """Test the method remove return True, because have 1 value"""
        board = Board()
        # Roll the dice
        die.roll()
        expected = True
        index = 1
        board.add(index, die.number)
        result = board.cad_remove(index)
        error_msg = f"Expected value: [{expected}]. Result= {result}"
        assert expected is result, error_msg

    def test_remove_all_values(self, die):
        """Test the method remove delete all the values of the dice"""
        board = Board()
        fake_die_val = 6
        index = 1
        # Add values
        board.add(index, fake_die_val)
        board.add(index, fake_die_val)
        # Then remove the value
        board.remove(index, fake_die_val)
        # Start test
        expected = 0
        col1 = board.get_column(index)
        result = len(col1)
        error_msg = f"Expected value: [{expected}]. Result= {result}"
        assert expected == result, error_msg

    def test_remove_all_values_and_left_one(self, die):
        """Test the method remove delete all the values of the dice"""
        board = Board()
        fake_die_val = 6
        other_fake_die_val = 3
        index = 1
        # Add values
        board.add(index, fake_die_val)
        board.add(index, fake_die_val)
        board.add(index, other_fake_die_val)  # This is the other value
        # Then remove the value
        board.remove(index, fake_die_val)
        # Start test
        expected = 1
        col1 = board.get_column(index)
        result = len(col1)
        error_msg = f"Expected value: [{expected}]. Result= {result}"
        assert expected == result, error_msg

    def test_is_not_full(self):
        board = Board()
        fake_die_val = 6
        board.add(1, fake_die_val)
        board.add(2, fake_die_val)
        board.add(3, fake_die_val)
        # Start test:
        expected = False
        result = board.is_full
        error_msg = f"Expected value: [{expected}]. Result= {result}"
        assert expected is result, error_msg

    def test_is_full(self):
        board = Board()
        fake_die_val = 6
        # Column 1
        board.add(1, fake_die_val)
        board.add(1, fake_die_val)
        board.add(1, fake_die_val)
        # Column 2
        board.add(2, fake_die_val)
        board.add(2, fake_die_val)
        board.add(2, fake_die_val)
        # Column 3
        board.add(3, fake_die_val)
        board.add(3, fake_die_val)
        board.add(3, fake_die_val)
        # Start test:
        expected = True
        result = board.is_full
        error_msg = f"Expected value: [{expected}]. Result= {result}"
        assert expected is result, error_msg

    def test_invalid_column_error_on_get(self):
        """Test InvalidColumnError is raised when getting an invalid column"""
        board = Board()
        invalid_column_index = 4  # an invalid column index
        expected_error_msg = f'This is a invalid column index: {invalid_column_index}'
        with pytest.raises(InvalidColumnError, match=expected_error_msg):
            board.get_column(invalid_column_index)

    def test_add_error(self):
        """Test AddError is raised when adding more values than allowed"""
        board = Board()
        valid_column_index = 1
        # Fill the column to the max
        board.add(valid_column_index, 1)
        board.add(valid_column_index, 2)
        board.add(valid_column_index, 3)
        expected_error_msg = f"You can't add more values in the Board Column: {valid_column_index}"
        with pytest.raises(AddError, match=expected_error_msg):
            board.add(valid_column_index, 4)  # adding one more than allowed

    def test_invalid_column_error_on_remove(self):
        """Test InvalidColumnError is raised when removing from an invalid column"""
        board = Board()
        invalid_column_index = 4  # an invalid column index
        expected_error_msg = f"You can't remove more values in the Board Column: {invalid_column_index}"
        with pytest.raises(RemoveError, match=expected_error_msg):
            board.remove(invalid_column_index, 1)

    def test_score_in_columns_3_equal_number(self):
        """Validate the ColumnScore Classe return valid point score"""
        board = Board()
        index = 1
        board.add(index, 2)
        board.add(index, 2)
        board.add(index, 2)
        expected = 18
        result = board.update_score(index).val
        error_msg = f"Expected value: [{expected}]. Result= {result}"
        assert expected == result, error_msg

    def test_score_in_columns_2_equal_number(self):
        """Validate the ColumnScore Classe return valid point score"""
        board = Board()
        index = 1
        board.add(index, 1)
        board.add(index, 1)
        expected = 4
        result = board.update_score(index).val
        error_msg = f"Expected value: [{expected}]. Result= {result}"
        assert expected == result, error_msg

    def test_score_in_columns_1_equal_number(self):
        """Validate the ColumnScore Classe return valid point score"""
        board = Board()
        index = 1
        board.add(index, 1)
        expected = 1
        result = board.update_score(index).val
        error_msg = f"Expected value: [{expected}]. Result= {result}"
        assert expected == result, error_msg

    def test_score_in_columns_2_equal_number_and_1_other_number(self):
        """Validate the ColumnScore Classe return valid point score"""
        board = Board()
        index = 1
        board.add(index, 1)  # 2
        board.add(index, 1)  # 2
        board.add(index, 2)  # 2
        expected = 6
        result = board.update_score(index).val
        error_msg = f"Expected value: [{expected}]. Result= {result}"
        assert expected == result, error_msg

    def test_score_in_columns_1_equal_number_and_2_other_number(self):
        """Validate the ColumnScore Classe return valid point score"""
        board = Board()
        index = 1
        board.add(index, 1)  # 1
        board.add(index, 2)  # 2
        board.add(index, 3)  # 3
        expected = 6
        result = board.update_score(index).val
        error_msg = f"Expected value: [{expected}]. Result= {result}"
        assert expected == result, error_msg

    def test_score_in_columns_not_values(self):
        """Validate the ColumnScore Classe return valid point score"""
        board = Board()
        index = 1
        expected = 0
        result = board.update_score(index).val
        error_msg = f"Expected value: [{expected}]. Result= {result}"
        assert expected == result, error_msg

    def test_score_in_columns_values_reset_after_removed(self):
        """Validate the ColumnScore Classe return valid point score"""
        board = Board()
        index = 1
        board.add(index, 1)  # 1
        board.add(index, 2)  # 2
        board.add(index, 3)  # 3
        # need to update values to have the new ones
        _ = board.update_score(index)
        # Then removed the current values and next updated again
        board.remove(index, 2)
        expected = 4
        result = board.update_score(index).val
        error_msg = f"Expected value: [{expected}]. Result= {result}"
        assert expected == result, error_msg

    def test_score_in_columns_values_reset_after_removed_all(self):
        """Validate the ColumnScore Classe return valid point score"""
        board = Board()
        index = 1
        board.add(index, 2)
        board.add(index, 2)
        board.add(index, 2)
        # need to update values to have the new ones
        _ = board.update_score(index)
        # Then removed the current values and next updated again
        board.remove(index, 2)
        expected = 0
        result = board.update_score(index).val
        error_msg = f"Expected value: [{expected}]. Result= {result}"
        assert expected == result, error_msg
