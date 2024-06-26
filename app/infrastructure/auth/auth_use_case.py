from fastapi import HTTPException, status
from firebase_admin import auth

from app.domain.auth.errors.errors import GoogleUserNotExit
from app.domain.auth.schemas.response import (ResponseSignin, ResponseLogIn, ResponseUsersRanking,
                                              ResponseUpdateUserNameAndLastName, ResponseUserRank)
from app.domain.auth.use_cases.i_auth_handler import IAuthHandler
from app.domain.auth.use_cases.i_auth_use_case import IAuthUseCase
from app.repositories.auth.auth_repository import AuthRepository


class AuthUseCase(IAuthUseCase):
    repo: AuthRepository

    def signin_with_google(self, google_user_id: str, auth_handler: IAuthHandler) -> ResponseSignin:
        try:
            user_google = auth.get_user(google_user_id)
        except Exception:
            raise GoogleUserNotExit('The userId Provider by the client not exist in Firebase.')

        user = self.repo.get_user(user_google.email)

        if not user:
            return self.signin(user_google.email, user_google.display_name, 'passwordFake', auth_handler)

        user.user_level = self.repo.get_user_level(user.user_id)
        user.bank_account = self.repo.get_user_bank_account(user.user_id)
        session_token = auth_handler.encode_token(user.user_id)
        return ResponseLogIn(user=user, session_token=session_token)

    def signin(self, email: str, name: str, password: str, auth_handler: IAuthHandler) -> ResponseSignin:
        user = self.repo.get_user(email)
        # If user don't exist created
        if not user:
            hash_password = auth_handler.get_password_hash(password)
            # Create new user with Hash Password
            # Convert the bytecode password into a string
            self.repo.create_user(email, name, hash_password.decode('utf-8'))
            # Get User to Create the new bank account and level progress
            user = self.repo.get_user(email)
            self.repo.create_user_level(user.user_id)
            self.repo.create_user_bank_account(user.user_id)

        # Check user hash password
        return self.login(email, password, auth_handler)

    def login(self, email: str, password: str, auth_handler: IAuthHandler) -> ResponseLogIn:
        user = self.repo.get_user(email)
        # Convert String into bytecodes to very the password
        # without this the method have error.
        if not user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User or Password have error.'
            )

        hash_password = user.password.get_secret_value().encode("utf-8")
        # [Error] if not user or the password verification fail
        if not user or not auth_handler.verify_password(password, hash_password):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User or Password have error.'
            )
        # Get the User Level and Bank account to create the Response
        user.user_level = self.repo.get_user_level(user.user_id)
        user.bank_account = self.repo.get_user_bank_account(user.user_id)
        session_token = auth_handler.encode_token(user.user_id)
        return ResponseLogIn(user=user, session_token=session_token)

    def login_from_session_token(self, user_id: str, auth_handler: IAuthHandler) -> ResponseLogIn:
        user = self.repo.get_user_by_id(user_id)
        user.user_level = self.repo.get_user_level(user.user_id)
        user.bank_account = self.repo.get_user_bank_account(user.user_id)
        session_token = auth_handler.encode_token(user.user_id)
        return ResponseLogIn(user=user, session_token=session_token)

    def update_user_name_and_last_name(self, user_id: str, name: str,
                                       last_name: str) -> ResponseUpdateUserNameAndLastName:
        self.repo.update_user_name_and_last_name(user_id, name, last_name)
        user = self.repo.get_user_by_id(user_id)
        return ResponseUpdateUserNameAndLastName(user=user)

    def get_users_ranking(self) -> ResponseUsersRanking:
        users_ranks = self.repo.get_users_ranking()
        return ResponseUsersRanking(users_ranks=users_ranks)

    def get_user_ranking(self, user_id: str) -> ResponseUserRank:
        user_rank = self.repo.get_user_ranking(user_id)
        return ResponseUserRank(user_rank=user_rank)

    def get_users_ranking_by_rank(self, rank_id: int) -> ResponseUsersRanking:
        users_ranks = self.repo.get_users_ranking_by_rank(rank_id)
        return ResponseUsersRanking(users_ranks=users_ranks)

    def get_user_ranking_by_rank(self, rank_id: int, user_id: str) -> ResponseUserRank:
        user_rank = self.repo.get_user_ranking_by_rank(rank_id, user_id)
        return ResponseUserRank(user_rank=user_rank)
