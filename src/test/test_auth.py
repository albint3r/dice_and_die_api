import pytest
from fastapi import status
from starlette.testclient import TestClient

from credentials_provider import credentials_provider
from src.db.db import _DataBase
from src.domain.auth.bank_account import BankAccount
from src.domain.auth.i_auth_facade import IAuthFacade
from src.domain.auth.user import User
from src.domain.auth.user_level import UserLevel
from src.infrastructure.auth.auth_facade_impl import AuthFacadeImpl
from src.main import app
from src.repositories.auth.auth_handler_impl import auth_handler, _AuthHandlerImpl
from src.repositories.auth.auth_repository import AuthRepository

client = TestClient(app=app)
email = 'test_user@teste.com'
password = 'test12345'


class TestAuth:

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
    def auth_handler_impl(self) -> _AuthHandlerImpl:
        return auth_handler

    def test_db_connection(self, db):
        """Test DB connects correctly"""
        # First test:
        error_msg = f"Expected value: [_DataBase]. Result= {db}"
        assert isinstance(db, _DataBase), error_msg

    def test_db_6_tables_exist(self, db):
        """Test DB connects correctly"""
        # First test:
        expected = 6
        test_query = 'SHOW TABLES;'
        response = db.query(test_query, fetch_all=True)
        result = len(response)
        error_msg = f"Expected value: [{expected}]. Result= {result}"
        assert expected == result, error_msg

    def test_signin_create_new_user(self, facade, auth_handler_impl, db):
        """Test if the method create a new user."""

        response = facade.signin(email, password, auth_handler)
        user = response.user
        # Check New User Exist:
        error_msg = f"Expected value: [User]. Result= {type(user)}"
        assert isinstance(user, User), error_msg
        # Check have Level:
        user_level = user.user_level
        error_msg = f"Expected value: [UserLevel]. Result= {type(user_level)}"
        assert isinstance(user_level, UserLevel), error_msg
        # Check have BankAccount:
        bank_account = user.bank_account
        error_msg = f"Expected value: [BankAccount]. Result= {type(bank_account)}"
        assert isinstance(bank_account, BankAccount), error_msg

    def test_user_login(self, facade, auth_handler_impl, db):
        """Test if the method create a new user."""
        expected_email = email
        response = facade.login(expected_email, password, auth_handler)
        user = response.user
        result_mail = user.email
        # Check New User Exist:
        error_msg = f"Expected value: [{expected_email}]. Result= [{result_mail}]"
        assert expected_email == result_mail, error_msg
        # Check User Level:
        user_level = user.user_level
        # Start Level equal to 0
        expected = 0
        result = user_level.level
        error_msg = f"Expected value: [{expected}]. Result= [{result}]"
        assert expected == result, error_msg
        # RankID equal 1
        expected = 1
        result = user_level.rank_id
        error_msg = f"Expected value: [{expected}]. Result= [{result}]"
        assert expected == result, error_msg
        # Check bank account:
        bank_account = user.bank_account
        # Started Amount 0
        expected = 0
        result = bank_account.amount
        error_msg = f"Expected value: [{expected}]. Result= [{result}]"
        assert expected == result, error_msg
        # Delete New User:
        facade.repo.delete_user(user.user_id)

    def test_api_signin(self):
        """Check if the api sign a new user"""
        # Setup
        json_data = {"email": email, 'password': password}
        expected = status.HTTP_201_CREATED
        response = client.post('/auth/v1/signin', json=json_data)
        error_msg = f'1-Expected Value: [{expected}] and result:[{response}]'
        assert expected == response.status_code == expected, error_msg

    def test_api_session_token_200_ok(self, facade):
        json_data = {"email": email, 'password': password}
        # First logIn to get the session token
        response = client.post('/auth/v1/login', json=json_data)
        json_data = response.json()
        # Extract token to testing:
        session_token = json_data.get('session_token')
        headers = {
            "accept": "application/json",
            "Authorization": 'Bearer ' + session_token
        }
        # Validate if user could enter to their session
        expected = status.HTTP_200_OK
        response = client.post('/auth/v1/test', headers=headers)
        error_msg = f'1-Expected Value: [{expected}] and result:[{response.status_code}]'
        assert expected == response.status_code, error_msg
        # DELETE USER:
        user_id = response.json()
        facade.repo.delete_user(user_id)

    def test_api_session_token_error(self):
        # Extract token to testing:
        session_token = 'THIS_IS_NOT_A_VALID_SESSION_TOKEN'
        headers = {
            "accept": "application/json",
            "Authorization": 'Bearer ' + session_token
        }
        # Validate if user could enter to their session
        expected = status.HTTP_401_UNAUTHORIZED
        response = client.post('/auth/v1/test', headers=headers)
        error_msg = f'1-Expected Value: [{expected}] and result:[{response.status_code}]'
        assert expected == response.status_code, error_msg
