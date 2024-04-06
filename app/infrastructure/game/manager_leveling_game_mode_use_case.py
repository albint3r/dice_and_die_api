from app.domain.auth.entities.user import User
from app.domain.game.enums.game_mode import RematchMode
from app.domain.game.use_cases.i_user_level_use_case import IManagerLevelingUseCase
from app.infrastructure.game.formulas import next_level_basic_formula


class ManagerLevelingGameModeUseCase(IManagerLevelingUseCase):
    _base_win_points: int = 20

    def get_winner_earned_exp_points(self, p1_score: int, p2_score: int, player_score: int,
                                     rematch_mode: RematchMode) -> int:

        if rematch_mode == RematchMode.n_best:
            return abs(p1_score - p2_score) * player_score * self._base_win_points
        if rematch_mode == RematchMode.best_total_games_score:
            return abs(p1_score - p2_score) * 2

    def get_winner_earned_exp_after_player_disconnect(self) -> int:
        return self._base_win_points * 3

    def update_user_level(self, user: User, exp_points: int) -> User:
        """Update User Level after win.
        In this facade the user level will be updated on:
        - Xp points
        - Level
        - Rank

        If any of these conditions apply it will the user entity and returned.
        """
        user.user_level.exp_points = self.leve_manager.add_exp_points(user.user_level, exp_points)
        ready_to_level_up = self.leve_manager.ready_to_progress(user_level=user.user_level,
                                                                formula=next_level_basic_formula)
        if ready_to_level_up:
            # Before update the user level We need to get the difference of the remaining points
            # Example:
            # Level to needed to level up: 50 exp
            # You have current exp: 40 + win_exp: 30 = 70
            # You have a difference of 20 (your exp: 70 - 50) point for the level to block.
            exp_points_diff = abs(user.user_level.exp_points - user.user_level.next_level_points)
            user.user_level.exp_points = exp_points_diff
            user.user_level = self.leve_manager.progress(user_level=user.user_level, formula=next_level_basic_formula)
            user.user_level.exp_points = abs(user.user_level.next_level_points - exp_points_diff)
            # User can upgrade rank?
            ready_to_rank_up = self.rank_manager.ready_to_progress(user_level=user.user_level)
            if ready_to_rank_up:
                user.user_level = self.rank_manager.progress(user.user_level)

        return user
