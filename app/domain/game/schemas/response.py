from pydantic import BaseModel, field_validator

from app.domain.core.ref_types import TExtras
from app.domain.game.entities.game import Game
from app.domain.game.errors.errors import NoneGameInResponseValidatorError


class GameResponse(BaseModel):
    """This is the Base Game Response"""
    game: Game
    extras: TExtras
    message: str

    @field_validator("game")
    def validator_game(cls, game):
        """Validate is a new [Game] instance."""
        if isinstance(game, Game):
            return game
        raise NoneGameInResponseValidatorError(f"To send a Game Response to listeners you must have an Game instances."
                                               f" But you have: {game}. This error is common after one user leave"
                                               f"the game and the remaining player is still in the game sending events.")
