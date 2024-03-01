from pydantic import BaseModel


class UserRank(BaseModel):
    ranking: int
    name: str = ''
    last_name: str
    level: int
    exp_points: int
    rank_id: int
