from pydantic import BaseModel, Field

from src.domain.user_level_manager.rank import Rank


class UserLevel(BaseModel):
    user_level_id: str = Field(exclude=True, repr=False)
    user_id: str = Field(exclude=True, repr=False)
    rank_id: int
    level: int
    exp_points: int
    next_level_points: int

    @property
    def rank(self) -> Rank:
        return Rank(self.rank_id)
