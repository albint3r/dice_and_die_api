from pydantic import validate_call

from src.domain.auth.user_level import UserLevel
from src.domain.core.i_game_manager import IGameManager
from src.domain.user_level_manager.rank import Rank


class _RankManager(IGameManager):

    @validate_call()
    def next_rank(self, rank: Rank) -> int:
        """Get the Level the user need to rank up.
        Example: The user is STONE, so he needs to be level 5 to pass to IRON.
        """
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

    @validate_call()
    def ready_to_rank_up(self, user_level: UserLevel) -> bool:
        """Check if the user have equal or more point to upgrade to the next Rank"""
        level_to_next_rank = self.next_rank(user_level.rank)
        return user_level.level >= level_to_next_rank

    @validate_call()
    def add_rank_up(self, user_level: UserLevel) -> UserLevel:
        """Add experience level """
        user_level.rank_id += 1
        return user_level


rank_manager = _RankManager()
