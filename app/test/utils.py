from datetime import datetime

from pydantic import SecretStr

from app.domain.auth.entities.bank_account import BankAccount
from app.domain.auth.entities.user import User
from app.domain.auth.entities.user_level import UserLevel
from app.domain.auth.enums.rank import Rank


def create_fake_p1() -> User:
    """Function to quickly create a test user with all fields populated."""
    creation_date = datetime.now()
    return User(
        creation_date=creation_date,
        user_id="1",
        email="test@example.com",
        password=SecretStr(secret_value='FAKE_PASSWORD'),
        name="John",
        last_name="Doe",
        is_verify=True,
        user_level=UserLevel(
            user_level_id="some_level_id",
            user_id="some_user_id",
            rank_id=Rank.STONE.value,
            level=1,
            exp_points=0,
            next_level_points=100
        ),
        bank_account=BankAccount(
            creation_date=creation_date,
            bank_account_id="some_account_id",
            user_id="some_user_id",
            amount=1000.0
        )
    )


def create_fake_p2() -> User:
    """Function to quickly create a test user with all fields populated."""
    creation_date = datetime.now()
    return User(
        creation_date=creation_date,
        user_id="2",
        email="test2@example.com",
        password=SecretStr(secret_value='ANOTHER_FAKE_PASSWORD'),
        name="Jane",
        last_name="Doe",
        is_verify=True,
        user_level=UserLevel(
            user_level_id="another_level_id",
            user_id="another_user_id",
            rank_id=Rank.BRONZE.value,
            level=2,
            exp_points=50,
            next_level_points=150
        ),
        bank_account=BankAccount(
            creation_date=creation_date,
            bank_account_id="another_account_id",
            user_id="another_user_id",
            amount=2000.0
        )
    )
