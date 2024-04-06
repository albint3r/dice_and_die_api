from math import ceil

from pydantic import BaseModel, Field

from app.domain.game.entities.player import Player
from app.domain.game.enums.game_mode import GameMode, RematchMode

TWinCounter = dict[str, int]


class GameConfig(BaseModel):
    game_mode: GameMode
    rematch_mode: RematchMode
    winner_player: tuple[Player, Player | None] | None = None
    is_game_mode_over: bool = False
    col_length: int = 3
    total_columns: int = 3
    total_games: int = 3
    wins_counter: TWinCounter = {}
    confirmed_players: set[str] = Field(default_factory=set)
    games_counter: int = 0

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
        self.games_counter += 1
        if self.rematch_mode == RematchMode.n_best:
            self.wins_counter[user_id] = self.wins_counter.get(user_id, 0) + 1
        if self.rematch_mode == RematchMode.best_total_games_score:
            self.wins_counter[user_id] = self.wins_counter.get(user_id, 0) + player.board.score

    def get_winner(self, game):  # noqa
        p1_score = game.config.wins_counter.get(game.p1.user.user_id, 0)
        p2_score = game.config.wins_counter.get(game.p2.user.user_id, 0)
        if p1_score > p2_score:
            winner_player, tied_player = (game.p1, None)
        elif p2_score > p1_score:
            winner_player, tied_player = (game.p2, None)
        else:
            winner_player, tied_player = (game.p1, game.p2)

        return winner_player, tied_player

    def are_all_games_played(self) -> bool:
        """Check if the game mode is over"""
        if self.rematch_mode == RematchMode.n_best:
            target_n = ceil(self.total_games * .51)
            self.is_game_mode_over = any([c == target_n for c in self.wins_counter.values()])

        if self.rematch_mode == RematchMode.best_total_games_score:
            self.is_game_mode_over = self.games_counter >= self.total_games

        return self.is_game_mode_over
