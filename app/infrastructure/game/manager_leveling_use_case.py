from app.domain.game.use_cases.i_leveling_use_case import ILeveling
from app.domain.game.use_cases.i_user_level_use_case import IManagerLevelingUseCase
from src.domain.auth.user import User
from src.domain.game.game import Game


class ManagerLevelingUseCase(IManagerLevelingUseCase):
    _base_win_points: int = 15

    def get_winner_earned_exp_points(self, game: Game) -> int:
        return abs(game.p1.board.total_score - game.p2.board.total_score) + self.base_win_points

    def update_user_level(self,
                          user: User,
                          exp_points: int,
                          leve_manager: ILeveling,
                          rank_manager: ILeveling) -> User:
        """pass"""
