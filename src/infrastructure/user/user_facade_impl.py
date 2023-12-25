from src.domain.user.i_user_facade import IUserFacade
from src.domain.user.schemas import SchemaUpdateUserNameAndLastName, SchemaUsersRanks
from src.repositories.auth.auth_repository import AuthRepository
from src.repositories.user.user_repository import UserRepository


class UserFacadeImpl(IUserFacade):
    repo: UserRepository
    repo_auth: AuthRepository

    def update_user_name_and_last_name(self, user_id: str, name: str,
                                       last_name: str) -> SchemaUpdateUserNameAndLastName:
        self.repo.update_user_name_and_last_name(user_id, name, last_name)
        user = self.repo_auth.get_user_by_id(user_id)
        return SchemaUpdateUserNameAndLastName(user=user)

    def get_users_ranking(self) -> SchemaUsersRanks:
        users_ranks = self.repo.get_users_ranking()
        return SchemaUsersRanks(users_ranks=users_ranks)
