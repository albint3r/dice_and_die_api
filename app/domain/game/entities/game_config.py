from pydantic import BaseModel, Field

from app.domain.game.entities.player import Player
from app.domain.game.enums.game_mode import GameMode


class GameConfig(BaseModel):
    mode: GameMode
    is_game_mode_over: bool = False
    col_length: int = 3
    total_columns: int = 3
    total_games: int = 3
    win_counter: dict[str, int] = {}
    confirmed_players: set[str] = Field(default_factory=set)

    @property
    def is_rematch(self) -> bool:
        return len(self.confirmed_players) >= 2

    def confirm_player_rematch_game(self, player: Player) -> None:
        """Add the player to the user to confirm the rematch game"""
        if player.user.user_id not in self.confirmed_players:
            self.confirmed_players.add(player.user.user_id)

    def reset_confirmed_players_rematch_game(self) -> None:
        self.confirmed_players = set()
