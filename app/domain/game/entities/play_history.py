import uuid

from pydantic import BaseModel, Field
from datetime import datetime, time

from app.domain.game.entities.game import Game


class PlayHistory(BaseModel):
    creation_date: datetime = datetime.now()
    play_history_id: uuid.uuid4 = Field(default_factory=uuid.uuid4)
    duration: time
    p1: str
    p1_score: int
    p1_col_1_0: int = 0
    p1_col_1_1: int = 0
    p1_col_1_2: int = 0
    p1_col_2_0: int = 0
    p1_col_2_1: int = 0
    p1_col_2_2: int = 0
    p1_col_3_0: int = 0
    p1_col_3_1: int = 0
    p1_col_3_2: int = 0
    p2: str
    p2_score: int
    p2_col_1_0: int = 0
    p2_col_1_1: int = 0
    p2_col_1_2: int = 0
    p2_col_2_0: int = 0
    p2_col_2_1: int = 0
    p2_col_2_2: int = 0
    p2_col_3_0: int = 0
    p2_col_3_1: int = 0
    p2_col_3_2: int = 0

    @classmethod
    def from_game(cls, game: Game) -> 'PlayHistory':
        p1 = game.p1
        p2 = game.p2
        game_start = game.create_date
        game_end = datetime.now()
        time_diff = game_end - game_start
        time_diff_seconds = time_diff.seconds
        return cls(
            p1=p1.user.user_id,
            p1_score=p1.board.score,
            duration=time(second=time_diff_seconds),
            p1_col_1_0=cls.get_score_value(p1.board.columns.get(1).values, 0),
            p1_col_1_1=cls.get_score_value(p1.board.columns.get(1).values, 1),
            p1_col_1_2=cls.get_score_value(p1.board.columns.get(1).values, 2),
            p1_col_2_0=cls.get_score_value(p1.board.columns.get(2).values, 0),
            p1_col_2_1=cls.get_score_value(p1.board.columns.get(2).values, 1),
            p1_col_2_2=cls.get_score_value(p1.board.columns.get(2).values, 2),
            p1_col_3_0=cls.get_score_value(p1.board.columns.get(3).values, 0),
            p1_col_3_1=cls.get_score_value(p1.board.columns.get(3).values, 1),
            p1_col_3_2=cls.get_score_value(p1.board.columns.get(3).values, 2),
            p2=p2.user.user_id,
            p2_score=p2.board.score,
            p2_col_1_0=cls.get_score_value(p2.board.columns.get(1).values, 0),
            p2_col_1_1=cls.get_score_value(p2.board.columns.get(1).values, 1),
            p2_col_1_2=cls.get_score_value(p2.board.columns.get(1).values, 2),
            p2_col_2_0=cls.get_score_value(p2.board.columns.get(2).values, 0),
            p2_col_2_1=cls.get_score_value(p2.board.columns.get(2).values, 1),
            p2_col_2_2=cls.get_score_value(p2.board.columns.get(2).values, 2),
            p2_col_3_0=cls.get_score_value(p2.board.columns.get(3).values, 0),
            p2_col_3_1=cls.get_score_value(p2.board.columns.get(3).values, 1),
            p2_col_3_2=cls.get_score_value(p2.board.columns.get(3).values, 2),
        )

    @staticmethod
    def get_score_value(column: list[int], i: int) -> int:
        return column[i] if i < len(column) else 0
