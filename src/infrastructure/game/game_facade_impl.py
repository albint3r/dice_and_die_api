from random import choice
from typing import Any

from src.domain.core.i_websocket_manager import IWsManager
from src.domain.game.board import Board
from src.domain.game.die import Die
from src.domain.game.game import Game
from src.domain.game.i_game_facade import IGameWebSocketFacade
from src.domain.game.player import Player
from fastapi import WebSocket


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
        return Game()

    def new_player(self) -> Player:
        """Create a new player"""
        board1 = Board()
        die1 = Die()
        return Player(board=board1, die=die1)

    def join_waiting_room(self, game_id: str, player: Player) -> None:
        """Join player to the game"""
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

    async def create_or_join_game(self, game_id: str, websocket: WebSocket) -> tuple[Game, Player]:
        game = self.get_game(game_id)
        if not self.exist_game(game_id):
            # Create new game
            game = self.new_game()
            await self.ws_manager.connect(game_id, game, websocket)
            # Create Player 1
            player = self.new_player()
            self.join_waiting_room(game_id, player)
            await self.ws_manager.send_message(game_id, 'Player 1 Connected')
        else:
            # Create player 2
            player = self.new_player()
            if not self.is_full_room(game_id):
                self.join_waiting_room(game_id, player)
                # Select Player Start Order
                start_player = self.select_player_start(game)
                game.set_current_player(start_player)
                await self.ws_manager.connect(game_id, game, websocket)
                await self.ws_manager.send_message(game_id, 'Player 2 Connected')
        return game, player
