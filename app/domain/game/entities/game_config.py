from pydantic import BaseModel

from app.domain.game.enums.game_mode import GameMode


class GameConfig(BaseModel):
    mode: GameMode
