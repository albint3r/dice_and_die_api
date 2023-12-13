from src.domain.auth.user import User
from src.domain.core.i_game_manager import IGameManager
from src.domain.user_level_manager.i_user_level_manager_facade import IUserLevelManagerFacade
from src.infrastructure.user_level_manager.utils import next_level_basic_formula
from src.repositories.user_level_manager.user_level_manager_repository import UserLeveRepository


class UserLevelManagerFacadeImpl(IUserLevelManagerFacade):
    repo: UserLeveRepository

    def update_user_level(self, user: User, exp_points: int, *,
                          leve_manager: IGameManager,
                          rank_manager: IGameManager) -> User:
        """Update User Level after win.
        In this facade the user level will be updated in:
        - xp points
        - level
        - Rank
        If this conditions apply it will change it.
        """
        # Add User Points
        user.user_level.exp_points = leve_manager.add_exp_points(user.user_level, exp_points)
        # User can update lvl?
        ready_to_level_up = leve_manager.ready_to_level_up(user.user_level, formula=next_level_basic_formula)
        if ready_to_level_up:
            user.user_level = leve_manager.add_level_up(user.user_level)
            # User can upgrade rank?
            ready_to_rank_up = rank_manager.ready_to_rank_up(user.user_level)
            if ready_to_rank_up:
                user.user_level = rank_manager.add_rank_up(user.user_level)
        self.repo.update_user_level(user.user_level)

        return user
