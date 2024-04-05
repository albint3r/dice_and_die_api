from pydantic import BaseModel, Field

from app.domain.game.entities.player import Player
from app.domain.game.enums.game_mode import GameMode

TWinCounter = dict[str, int]


class GameConfig(BaseModel):
    mode: GameMode
    is_game_mode_over: bool = False
    col_length: int = 3
    total_columns: int = 3
    total_games: int = 3
    wins_counter: TWinCounter = {}
    confirmed_players: set[str] = Field(default_factory=set)

    @property
    def is_rematch(self) -> bool:
        """If both players are confirmed rematch the game."""
        return len(self.confirmed_players) >= 2

    def confirm_player_rematch_game(self, player: Player) -> None:
        """Add the player to the user to confirm the rematch game"""
        if player.user.user_id not in self.confirmed_players:
            self.confirmed_players.add(player.user.user_id)

    def reset_confirmed_players_rematch_game(self) -> None:
        """Reset the user that are ready for a rematch"""
        self.confirmed_players = set()

    def update_wins_counter(self, player: Player) -> None:
        """Update the record property to count how many wins have the player."""
        user_id = player.user.user_id
        self.wins_counter[user_id] = self.wins_counter.get(user_id, 0) + 1

    def are_all_games_played(self) -> bool:
        """Check if the game mode is over"""
        self.is_game_mode_over = sum(self.wins_counter.values()) == self.total_games
        return self.is_game_mode_over
