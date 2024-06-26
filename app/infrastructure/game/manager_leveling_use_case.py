from app.domain.auth.entities.user import User
from app.domain.game.entities.game import Game
from app.domain.game.use_cases.i_user_level_use_case import IManagerLevelingUseCase
from app.infrastructure.game.formulas import next_level_basic_formula


class ManagerLevelingUseCase(IManagerLevelingUseCase):
    _base_win_points: int = 15

    def get_winner_earned_exp_points(self, game: Game) -> int:
        return abs(game.p1.board.score - game.p2.board.score) + self._base_win_points # noqa

    def get_winner_earned_exp_after_player_disconnect(self) -> int:
        return self._base_win_points # noqa

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
            # Level to need 50 exp
            # You have 40 + 30 = 70
            # You have a difference of 20 point for the level to block.
            user.user_level.exp_points = user.user_level.exp_points - user.user_level.next_level_points
            user.user_level = self.leve_manager.progress(user_level=user.user_level, formula=next_level_basic_formula)
            # User can upgrade rank?
            ready_to_rank_up = self.rank_manager.ready_to_progress(user_level=user.user_level)
            if ready_to_rank_up:
                user.user_level = self.rank_manager.progress(user.user_level)

        return user
