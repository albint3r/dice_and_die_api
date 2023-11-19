from icecream import ic

from src.domain.board.board import Board
from src.domain.die.die import Die
from src.domain.player.player import Player


def run():
    die = Die()
    board = Board()
    player = Player(die=die, board=board)
    ic(player)


if __name__ == '__main__':
    run()
