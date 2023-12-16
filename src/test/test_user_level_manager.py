import pytest
from icecream import ic

from credentials_provider import credentials_provider
from src.db.db import _DataBase
from src.domain.auth.i_auth_facade import IAuthFacade
from src.domain.auth.user import User
from src.domain.user_level_manager.i_user_level_manager_facade import IUserLevelManagerFacade
from src.domain.user_level_manager.rank import Rank
from src.infrastructure.auth.auth_facade_impl import AuthFacadeImpl
from src.infrastructure.user_level_manager.level_manager import next_level_basic_formula, \
    level_manager, _LevelManager
from src.infrastructure.user_level_manager.rank_manager import rank_manager
from src.infrastructure.user_level_manager.user_level_manager_facade_impl import UserLevelManagerFacadeImpl
from src.infrastructure.user_level_manager.utils import next_level_advance_formula
from src.repositories.auth.auth_handler_impl import auth_handler
from src.repositories.auth.auth_repository import AuthRepository
from src.repositories.user_level_manager.user_level_manager_repository import UserLeveRepository

test_email = "test_user@test.com"
test_password = "test_password_12345"


class TestUserLevelManager:

    @pytest.fixture
    def db(self) -> _DataBase:
        db = _DataBase(user=credentials_provider.user, password=credentials_provider.password,
                       host='db', database='dice_and_die', port='3306')
        db.connect()
        return db

    @pytest.fixture
    def facade(self, db) -> IAuthFacade:
        return AuthFacadeImpl(repo=AuthRepository(db=db))

    @pytest.fixture
    def facade_ulm(self, db) -> IUserLevelManagerFacade:
        return UserLevelManagerFacadeImpl(repo=UserLeveRepository(db=db))

    @pytest.fixture
    def fake_user_1(self, facade) -> User:
        user_mail = 'fake_user1@gmail.com'
        # Create a new user
        user = facade.repo.get_user(user_mail)
        user.user_level = facade.repo.get_user_level(user.user_id)
        user.bank_account = facade.repo.get_user_bank_account(user.user_id)
        return user

    @pytest.fixture
    def user_level_manager_impl(self) -> _LevelManager:
        return _LevelManager()

    @pytest.fixture(autouse=True)
    def post_user_delete(self, facade, facade_ulm):
        """Validate User Win the points"""
        response = facade.signin(test_email, test_password, auth_handler)
        new_user = response.user
        facade.repo.delete_user(new_user.user_id)

    def test_next_level_formulas(self, fake_user_1, user_level_manager_impl):
        """Validate the fake User creation"""
        error_msg = f"Expected [User]. Result: [{fake_user_1}]"
        assert isinstance(fake_user_1, User), error_msg
        # Check basic formula
        expected = 50
        result = user_level_manager_impl.next_level(fake_user_1.user_level, formula=next_level_basic_formula)
        error_msg = f"Expected: {expected}. Result: {result}"
        assert expected == result, error_msg
        # Check Advance formula
        expected = 100
        result = user_level_manager_impl.next_level(fake_user_1.user_level, formula=next_level_advance_formula)
        error_msg = f"Expected: {expected}. Result: {result}"
        assert expected == result, error_msg

    def test_add_exp_points_not_save_level(self, fake_user_1, user_level_manager_impl):
        """Validate the fake User creation"""
        # Check basic formula
        exp_points = 50
        result = user_level_manager_impl.add_exp_points(fake_user_1.user_level, exp_points)
        expected = 50
        error_msg = f"1) Expected: {expected}. Result: {result}"
        assert expected == result, error_msg
        # Second test after add first points
        exp_points = 20
        result = user_level_manager_impl.add_exp_points(fake_user_1.user_level, exp_points)
        expected = 20
        error_msg = f"2) Expected: {expected}. Result: {result}"
        assert expected == result, error_msg
        # Third test after add the second points
        exp_points = 35  # Total 105
        result = user_level_manager_impl.add_exp_points(fake_user_1.user_level, exp_points)
        expected = 35
        error_msg = f"3) Expected: {expected}. Result: {result}"
        assert expected == result, error_msg

    def test_add_exp_points_yes_save_level(self, fake_user_1, user_level_manager_impl):
        """Validate the fake User creation"""
        # Check basic formula
        exp_points = 50
        fake_user_1.user_level.exp_points = user_level_manager_impl.add_exp_points(fake_user_1.user_level,
                                                                                   exp_points)
        result = fake_user_1.user_level.exp_points
        expected = 50
        error_msg = f"1) Expected: {expected}. Result: {result}"
        assert expected == result, error_msg
        # Second test after add first points
        exp_points = 20
        fake_user_1.user_level.exp_points = user_level_manager_impl.add_exp_points(fake_user_1.user_level,
                                                                                   exp_points)
        result = fake_user_1.user_level.exp_points
        expected = 70
        error_msg = f"2) Expected: {expected}. Result: {result}"
        assert expected == result, error_msg
        # Third test after add the second points
        exp_points = 35  # Total 105
        fake_user_1.user_level.exp_points = user_level_manager_impl.add_exp_points(fake_user_1.user_level,
                                                                                   exp_points)
        result = fake_user_1.user_level.exp_points
        expected = 105
        error_msg = f"3) Expected: {expected}. Result: {result}"
        assert expected == result, error_msg

    def test_ready_to_level_up_advance_formula(self, fake_user_1, user_level_manager_impl):
        """Validate the fake User creation"""
        # Check basic formula
        exp_points = 50
        fake_user_1.user_level.exp_points = user_level_manager_impl.add_exp_points(fake_user_1.user_level,
                                                                                   exp_points)
        result = user_level_manager_impl.ready_to_level_up(fake_user_1.user_level, formula=next_level_advance_formula)
        expected = False
        error_msg = f"1) Expected: {expected}. Result: {result}"
        assert expected is result, error_msg
        # User Pass the first threshold and have enough point to upgrade
        exp_points = 55
        fake_user_1.user_level.exp_points = user_level_manager_impl.add_exp_points(fake_user_1.user_level,
                                                                                   exp_points)
        result = user_level_manager_impl.ready_to_level_up(fake_user_1.user_level, formula=next_level_advance_formula)
        expected = True
        error_msg = f"2) Expected: {expected}. Result: {result}"
        assert expected is result, error_msg

    def test_ready_to_level_up_basic_formula(self, fake_user_1, user_level_manager_impl):
        """Validate the fake User creation"""
        # Check basic formula
        exp_points = 30
        fake_user_1.user_level.exp_points = user_level_manager_impl.add_exp_points(fake_user_1.user_level,
                                                                                   exp_points)
        result = user_level_manager_impl.ready_to_level_up(fake_user_1.user_level, formula=next_level_basic_formula)
        expected = False
        error_msg = f"1) Expected: {expected}. Result: {result}"
        assert expected is result, error_msg
        # User Pass the first threshold and have enough point to upgrade
        exp_points = 40
        fake_user_1.user_level.exp_points = user_level_manager_impl.add_exp_points(fake_user_1.user_level,
                                                                                   exp_points)
        result = user_level_manager_impl.ready_to_level_up(fake_user_1.user_level, formula=next_level_basic_formula)
        expected = True
        error_msg = f"2) Expected: {expected}. Result: {result}"
        assert expected is result, error_msg

    def test_win_player_update_points_no_level_up(self, facade, facade_ulm):
        """Validate User Win the points"""
        response = facade.signin(test_email, test_password, auth_handler)
        new_user = response.user
        exp_points = 30
        # Started Testing of the Update User Level Facade
        user = facade_ulm.update_user_level(new_user, exp_points, leve_manager=level_manager,
                                            rank_manager=rank_manager)
        expected = 30
        result = user.user_level.exp_points
        error_msg = f"1) Expected: {expected}. Result: {result}"
        assert expected == result, error_msg
        # Check not update level:
        expected = 1
        result = user.user_level.level
        error_msg = f"1) Expected: {expected}. Result: {result}"
        assert expected == result, error_msg
        # Delete Test user
        facade.repo.delete_user(user.user_id)

    def test_win_player_update_points_yes_level_up(self, facade, facade_ulm):
        """Validate User Win the points"""

        response = facade.signin(test_email, test_password, auth_handler)

        new_user = response.user
        exp_points = 105
        # Started Testing of the Update User Level Facade
        user = facade_ulm.update_user_level(new_user, exp_points, leve_manager=level_manager,
                                            rank_manager=rank_manager)
        expected = 104
        result = user.user_level.next_level_points
        error_msg = f"1) Expected: {expected}. Result: {result}"
        assert expected == result, error_msg
        # Check user level up:
        expected = 2
        result = user.user_level.level
        error_msg = f"2) Expected: {expected}. Result: {result}"
        assert expected == result, error_msg
        # Delete Test user
        facade.repo.delete_user(user.user_id)

    def test_win_player_update_points_rank_up(self, facade, facade_ulm):
        """Validate User Win the points"""
        response = facade.signin(test_email, test_password, auth_handler)
        new_user = response.user
        exp_points = 70
        # Iterate on each level until the user could rank
        user = None
        for i in range(1, 5):
            user = facade_ulm.update_user_level(new_user, exp_points * i,  # Multiply the exp point by the index
                                                leve_manager=level_manager,
                                                rank_manager=rank_manager)
            expected = i + 1
            result = user.user_level.level
            curren_points = user.user_level.exp_points
            next_lvl_points = user.user_level.next_level_points
            error_msg = f"1.{i}) Lvl Expected: {expected}. Lvl Result: {result}: " \
                        f"Current Points: {curren_points} -> next_lvl_points: {next_lvl_points}"
            assert expected == result, error_msg

        # Validate the user change rank after reach the lvl 5
        expected = Rank.IRON
        result = user.user_level.rank
        error_msg = f"2.1) Expected: {expected}. Result: {result}"
        # Delete Test user
        facade.repo.delete_user(new_user.user_id)
        assert expected == result, error_msg

    def test_reset_exp_points(self, facade, facade_ulm):
        """Validate User Win the points"""
        response = facade.signin(test_email, test_password, auth_handler)
        new_user = response.user
        facade.repo.delete_user(new_user.user_id)
        exp_point = 30
        user = facade_ulm.update_user_level(new_user, exp_point,
                                            leve_manager=level_manager,
                                            rank_manager=rank_manager)
        exp_point = 40
        user = facade_ulm.update_user_level(user, exp_point,
                                            leve_manager=level_manager,
                                            rank_manager=rank_manager)
        expected = 20
        result = user.user_level.exp_points
        error_msg = f"2.1) Expected: {expected}. Result: {result}"
        assert expected == result, error_msg
