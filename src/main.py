from src.infrastructure.game.game_facade_impl import GameFacadeImpl
from src.presentation.game.game import run_game


def run():
    run_game(GameFacadeImpl())


if __name__ == '__main__':
    run()
