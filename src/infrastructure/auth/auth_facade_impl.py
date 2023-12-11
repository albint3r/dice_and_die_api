from src.domain.auth.i_auth_facade import IAuthFacade
from src.repositories.auth.auth_repository import AuthRepository


class AuthFacadeImpl(IAuthFacade):
    repo: AuthRepository

    def signin(self, email: str, password: str):
        return self.repo.get_user(email, password)

    def login(self, email: str, password: str):
        pass

    def logout(self):
        pass
