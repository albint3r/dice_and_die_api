from src.domain.auth.user import User
from src.domain.user_level_manager.i_user_level_manager_facade import IUserLevelManagerFacade
from src.infrastructure.user_level_manager.user_level_manager import GameManager, next_level_basic_formula
from src.repositories.user_level_manager.user_level_manager_repository import UserLeveRepository


class UserLevelManagerFacadeImpl(IUserLevelManagerFacade):
    repo: UserLeveRepository

    def update_user_level(self, user: User, exp_points: int, game_manager: GameManager) -> User:
        # Add User Points
        user.user_level.exp_points = game_manager.add_exp_points(user.user_level, exp_points)
        # User can update lvl?
        ready_to_level_up = game_manager.ready_to_level_up(user.user_level, formula=next_level_basic_formula)
        if ready_to_level_up:
            user.user_level.level += 1
            # User can upgrade rank?
            # Todo: Add UPDATE RANK Function
        self.repo.update_user_level(user.user_level)

        return user
