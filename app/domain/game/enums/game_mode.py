from enum import Enum


class GameMode(Enum):
    CLASSIC: str = 'CLASSIC'
    ADVENTURE: str = 'ADVENTURE'


class RematchMode(Enum):
    n_best: str = 'n_best'
    best_total_games_score: str = 'best_total_games_score'
