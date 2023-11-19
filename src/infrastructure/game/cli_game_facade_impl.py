from random import choice

from src.domain.board.board import Board
from src.domain.die.die import Die
from src.domain.game.game import Game
from src.domain.game.i_game_facade import IGameFacade
from src.domain.player.player import Player


class CliGameFacadeImpl(IGameFacade):

    def select_column(self, player: Player) -> int:
        while True:
            try:
                col_index = int(input('Select column: '))
                if 1 <= col_index <= 3:
                    break
                else:
                    print('The value must be between 1 an 3.')
            except ValueError:
                print('Please enter an integer. Try again.')
        return col_index

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
