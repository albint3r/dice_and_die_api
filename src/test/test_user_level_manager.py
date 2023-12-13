import pytest
from icecream import ic

from credentials_provider import credentials_provider
from src.db.db import _DataBase
from src.domain.auth.i_auth_facade import IAuthFacade
from src.domain.auth.user import User
from src.infrastructure.auth.auth_facade_impl import AuthFacadeImpl
from src.infrastructure.user_level_manager.user_level_manager import UserLevelManager
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

    def test_fake_user_exist(self, fake_user_1, user_level_manager_impl):
        """Validate the fake User creation"""
        error_msg = f"Expected [User]. Result: [{fake_user_1}]"
        assert isinstance(fake_user_1, User), error_msg
        # Check next point for level up:
        fake_user_1.user_level.level = 2
        ic(user_level_manager_impl.next_level(fake_user_1.user_level))
        assert False
