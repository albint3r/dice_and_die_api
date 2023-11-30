from random import choice
from typing import Any

from src.domain.core.i_websocket_manager import IWsManager
from src.domain.game.board import Board
from src.domain.game.die import Die
from src.domain.game.game import Game
from src.domain.game.game_state import GameState
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

    def new_game(self, game_id: str) -> Game:
        # Create All the Assets for a new game
        return Game(id=game_id)

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

    def get_winner_player(self, game_id: str) -> None:
        game = self.ws_manager.get_game(game_id)
        p1 = game.p1
        p2 = game.p2
        game.winner_player = p1 if p1.board.total_score > p2.board.total_score else p2

    def exist_game(self, game_id: str) -> bool:
        game = self.ws_manager.get_game(game_id)
        return isinstance(game, Game)

    async def create_or_join_game(self, game_id: str, websocket: WebSocket) -> tuple[Game, Player]:
        game = self.get_game(game_id)
        if not self.exist_game(game_id):
            # Create new game
            game = self.new_game(game_id)
            await self.ws_manager.connect(game_id, game, websocket)
            # Create Player 1
            player = self.new_player()
            self.join_waiting_room(game_id, player)
            message = 'Player 1 Connected'
            await self.update_game(game_id, message)
        else:
            # Create player 2
            player = self.new_player()
            if not self.is_full_room(game_id):
                self.join_waiting_room(game_id, player)
                # Select Player Start Order
                start_player = self.select_player_start(game)
                game.set_current_player(start_player)
                await self.ws_manager.connect(game_id, game, websocket)
                message = 'Player 2 Connected'
                self.update_game_state(game, GameState.ROLL_DICE)
                await self.update_game(game_id, message)
        return game, player

    async def update_game(self, game_id: str, message: str) -> None:
        """Update the match board"""
        await self.ws_manager.send_match(game_id, message)

    def update_game_state(self, game: Game, new_state: GameState) -> None:
        """Update the state of the game"""
        if game.state != new_state:
            game.state = new_state

    async def get_player_event_message(self, websocket: WebSocket) -> str:
        import json
        response = await websocket.receive()
        text_dict = response.get('text')
        json_data = json.loads(text_dict)
        return json_data.get('message')
