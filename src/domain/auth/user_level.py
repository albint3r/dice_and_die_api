from pydantic import BaseModel, Field


class UserLevel(BaseModel):
    user_level_id: str = Field(exclude=True, repr=False)
    user_id: str = Field(exclude=True, repr=False)
    rank_id: int
    level: int
    current_points: int
    next_level_points: int
