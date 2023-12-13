import pytest
from icecream import ic

from credentials_provider import credentials_provider
from src.db.db import _DataBase
from src.domain.auth.i_auth_facade import IAuthFacade
from src.domain.auth.user import User
from src.infrastructure.auth.auth_facade_impl import AuthFacadeImpl
from src.infrastructure.user_level_manager.user_level_manager import UserLevelManager, next_level_basic_formula, \
    next_level_advance_formula
from src.repositories.auth.auth_handler_impl import auth_handler, _AuthHandlerImpl
from src.repositories.auth.auth_repository import AuthRepository


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
    def fake_user_1(self, facade) -> User:
        user_mail = 'fake_user1@gmail.com'
        # Create a new user
        user = facade.repo.get_user(user_mail)
        user.user_level = facade.repo.get_user_level(user.user_id)
        user.bank_account = facade.repo.get_user_bank_account(user.user_id)
        return user

    @pytest.fixture
    def user_level_manager_impl(self) -> UserLevelManager:
        return UserLevelManager()

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
        expected = 51
        error_msg = f"1) Expected: {expected}. Result: {result}"
        assert expected == result, error_msg
        # Second test after add first points
        exp_points = 20
        result = user_level_manager_impl.add_exp_points(fake_user_1.user_level, exp_points)
        expected = 21
        error_msg = f"2) Expected: {expected}. Result: {result}"
        assert expected == result, error_msg
        # Third test after add the second points
        exp_points = 35  # Total 105
        result = user_level_manager_impl.add_exp_points(fake_user_1.user_level, exp_points)
        expected = 36
        error_msg = f"3) Expected: {expected}. Result: {result}"
        assert expected == result, error_msg

    def test_add_exp_points_yes_save_level(self, fake_user_1, user_level_manager_impl):
        """Validate the fake User creation"""
        # Check basic formula
        exp_points = 50
        fake_user_1.user_level.current_points = user_level_manager_impl.add_exp_points(fake_user_1.user_level,
                                                                                       exp_points)
        result = fake_user_1.user_level.current_points
        expected = 51
        error_msg = f"1) Expected: {expected}. Result: {result}"
        assert expected == result, error_msg
        # Second test after add first points
        exp_points = 20
        fake_user_1.user_level.current_points = user_level_manager_impl.add_exp_points(fake_user_1.user_level,
                                                                                       exp_points)
        result = fake_user_1.user_level.current_points
        expected = 71
        error_msg = f"2) Expected: {expected}. Result: {result}"
        assert expected == result, error_msg
        # Third test after add the second points
        exp_points = 35  # Total 105
        fake_user_1.user_level.current_points = user_level_manager_impl.add_exp_points(fake_user_1.user_level,
                                                                                       exp_points)
        result = fake_user_1.user_level.current_points
        expected = 106
        error_msg = f"3) Expected: {expected}. Result: {result}"
        assert expected == result, error_msg

    def test_ready_to_level_up_advance_formula(self, fake_user_1, user_level_manager_impl):
        """Validate the fake User creation"""
        # Check basic formula
        exp_points = 50
        fake_user_1.user_level.current_points = user_level_manager_impl.add_exp_points(fake_user_1.user_level,
                                                                                       exp_points)
        result = user_level_manager_impl.ready_to_level_up(fake_user_1.user_level, formula=next_level_advance_formula)
        expected = False
        error_msg = f"1) Expected: {expected}. Result: {result}"
        assert expected is result, error_msg
        # User Pass the first threshold and have enough point to upgrade
        exp_points = 55
        fake_user_1.user_level.current_points = user_level_manager_impl.add_exp_points(fake_user_1.user_level,
                                                                                       exp_points)
        result = user_level_manager_impl.ready_to_level_up(fake_user_1.user_level, formula=next_level_advance_formula)
        expected = True
        error_msg = f"1) Expected: {expected}. Result: {result}"
        assert expected is result, error_msg

    def test_ready_to_level_up_basic_formula(self, fake_user_1, user_level_manager_impl):
        """Validate the fake User creation"""
        # Check basic formula
        exp_points = 30
        fake_user_1.user_level.current_points = user_level_manager_impl.add_exp_points(fake_user_1.user_level,
                                                                                       exp_points)
        result = user_level_manager_impl.ready_to_level_up(fake_user_1.user_level, formula=next_level_basic_formula)
        expected = False
        error_msg = f"1) Expected: {expected}. Result: {result}"
        assert expected is result, error_msg
        # User Pass the first threshold and have enough point to upgrade
        exp_points = 40
        fake_user_1.user_level.current_points = user_level_manager_impl.add_exp_points(fake_user_1.user_level,
                                                                                       exp_points)
        result = user_level_manager_impl.ready_to_level_up(fake_user_1.user_level, formula=next_level_basic_formula)
        expected = True
        error_msg = f"1) Expected: {expected}. Result: {result}"
        assert expected is result, error_msg
