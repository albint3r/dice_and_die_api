from pydantic import BaseModel


class UserRank(BaseModel):
    name: str
    last_name: str
    level: int
    exp_points: int
    rank_id: int
