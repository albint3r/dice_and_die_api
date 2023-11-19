from icecream import ic

from src.domain.board.board import Board
from src.domain.die.die import Die
from src.domain.game.game import Game
from src.domain.game.i_game_facade import IGameFacade
from src.domain.player.player import Player
from random import choice


class GameFacadeImpl(IGameFacade):

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

    def run(self) -> None:
        game = self.new_game()
        start_player = self.select_player_start(game)
        game.set_current_player(start_player)
        ic(start_player.is_same_player(game.p1))
