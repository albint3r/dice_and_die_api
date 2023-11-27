from random import choice
from typing import Any

from src.domain.core.i_websocket_manager import IWsManager
from src.domain.game.board import Board
from src.domain.game.die import Die
from src.domain.game.game import Game
from src.domain.game.i_game_facade import IGameFacade, IGameWebSocketFacade
from src.domain.game.player import Player


class GameFacadeImpl(IGameWebSocketFacade):
    ws_manager: IWsManager

    def select_column(self, json: Any) -> int:
        user_input = json['message']
        try:
            return int(user_input)
        except ValueError:
            return 0

    def select_player_start(self, game: Game) -> Player:
        players_order = [game.p1, game.p2]
        return choice(players_order)

    def new_game(self) -> Game:
        # Create All the Assets for a new game
        # Player one
        board1 = Board()
        die1 = Die()
        p1 = Player(board=board1, die=die1)
        # Player two
        board2 = Board()
        die2 = Die()
        p2 = Player(board=board2, die=die2)
        return Game(p1=p1, p2=p2)

    def join_waiting_room(self, game_id: str, player: Player) -> None:
        game = self.ws_manager.get_game(game_id)
        if not game.p1:
            game.p1 = player
            return
        game.p2 = player

    def is_full_room(self, game_id: str) -> bool:
        """Validate the game have two players."""
        return self.ws_manager.is_game_full(game_id)

    def get_game(self, game_id: str) -> Game:
        return self.ws_manager.get_game(game_id)

    def exist_game(self, game_id: str) -> bool:
        game = self.ws_manager.get_game(game_id)
        return isinstance(game, Game)

    def new_game2(self) -> Game:
        return Game()

    def new_player(self) -> Player:
        board1 = Board()
        die1 = Die()
        return Player(board=board1, die=die1)
