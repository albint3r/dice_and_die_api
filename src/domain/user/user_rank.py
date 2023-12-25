from pydantic import BaseModel

from src.domain.user_level_manager.rank import Rank


class UserRank(BaseModel):
    name: str
    last_name: str
    level: int
    exp_points: int
    rank_id: int
