from app.domain.game.use_cases.i_leveling_use_case import ILeveling, IRankUseCase, ILevelUseCase
from app.domain.game.use_cases.i_user_level_use_case import IManagerLevelingUseCase
from app.infrastructure.game.formulas import next_level_basic_formula
from src.domain.auth.user import User
from src.domain.game.game import Game


class ManagerLevelingUseCase(IManagerLevelingUseCase):
    _base_win_points: int = 15

    def get_winner_earned_exp_points(self, game: Game) -> int:
        return abs(game.p1.board.total_score - game.p2.board.total_score) + self.base_win_points

    def update_user_level(self,
                          user: User,
                          exp_points: int,
                          leve_manager: ILevelUseCase,
                          rank_manager: IRankUseCase) -> User:
        """Update User Level after win.
        In this facade the user level will be updated on:
        - Xp points
        - Level
        - Rank

        If any of these conditions apply it will the user entity and returned.
        """
        user.user_level.exp_points = leve_manager.add_exp_points(user.user_level, exp_points)
        ready_to_level_up = leve_manager.ready_to_progress(user_level=user.user_level, formula=next_level_basic_formula)
        if ready_to_level_up:
            # Before update the user level We need to get the difference of the remaining points
            # Example:
            # Level to need 50 exp
            # You have 40 + 30 = 70
            # You have a difference of 20 point for the level to block.
            user.user_level.exp_points = user.user_level.exp_points - user.user_level.next_level_points
            user.user_level = leve_manager.progress(user_level=user.user_level, formula=next_level_basic_formula)
            # User can upgrade rank?
            ready_to_rank_up = rank_manager.ready_to_progress(user_level=user.user_level)
            if ready_to_rank_up:
                user.user_level = rank_manager.ready_to_progress(user.user_level)

        return user
