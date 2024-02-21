from app.domain.auth.entities.user_level import UserLevel
from app.domain.auth.enums.rank import Rank
from app.domain.game.use_cases.i_progress_use_case import IRankUseCase


class RankUseCase(IRankUseCase):
    def next_stage(self, rank: Rank) -> int:
        match rank:
            case Rank.STONE:
                return 5
            case Rank.IRON:
                return 10
            case Rank.BRONZE:
                return 20
            case Rank.SILVER:
                return 30
            case Rank.GOLD:
                return 50
            case Rank.PLATINUM:
                return 75
            case Rank.DIAMOND:
                return 100

    def ready_to_progress(self, user_level: UserLevel) -> bool:
        level_to_next_rank = self.next_stage(user_level.rank)
        return user_level.level >= level_to_next_rank

    def progress(self, user_level: UserLevel):
        user_level.rank_id += 1
        return user_level
