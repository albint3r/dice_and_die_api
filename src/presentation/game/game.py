from src.domain.game.i_game_facade import IGameFacade


def run_game(facade: IGameFacade):
    facade.run()
