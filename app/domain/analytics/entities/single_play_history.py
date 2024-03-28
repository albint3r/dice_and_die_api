from datetime import datetime

from pydantic import BaseModel, Field

from app.domain.game.entities.game import Game


class SinglePlayHistory(BaseModel):
    creation_date: datetime = Field(default_factory=datetime.now)
    game_id: str
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
    dice_result: int = 0
    column_index: int = 0

    @classmethod
    def from_game(cls, game: Game, column_index: int) -> 'SinglePlayHistory':
        p1 = game.current_player
        p2 = game.get_opponent_player()
        return cls(
            game_id=game.game_id,
            p1_score=p1.board.score,
            p1_col_1_0=cls.get_score_value(p1.board.columns.get(1).values, 0),
            p1_col_1_1=cls.get_score_value(p1.board.columns.get(1).values, 1),
            p1_col_1_2=cls.get_score_value(p1.board.columns.get(1).values, 2),
            p1_col_2_0=cls.get_score_value(p1.board.columns.get(2).values, 0),
            p1_col_2_1=cls.get_score_value(p1.board.columns.get(2).values, 1),
            p1_col_2_2=cls.get_score_value(p1.board.columns.get(2).values, 2),
            p1_col_3_0=cls.get_score_value(p1.board.columns.get(3).values, 0),
            p1_col_3_1=cls.get_score_value(p1.board.columns.get(3).values, 1),
            p1_col_3_2=cls.get_score_value(p1.board.columns.get(3).values, 2),
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
            dice_result=p1.die.current_number,
            column_index=column_index
        )

    @staticmethod
    def get_score_value(column: list[int], i: int) -> int:
        return column[i] if i < len(column) else 0
