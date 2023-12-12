from pydantic import BaseModel, Field


class UserLevel(BaseModel):
    user_level_id: str = Field(exclude=True)
    user_id: str = Field(exclude=True)
    rank_id: int = 1
    level: int = 0
    current_points: int = 0
    next_level_points: int = 100
