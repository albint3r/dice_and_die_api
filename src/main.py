from src.infrastructure.game.cli_game_facade_impl import CliGameFacadeImpl
from src.presentation.game.game import run_game


def run():
    run_game(CliGameFacadeImpl())


if __name__ == '__main__':
    run()
