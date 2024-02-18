from random import choice
from typing import Any

from fastapi import WebSocket
from icecream import ic

from src.domain.auth.user import User
from src.domain.core.i_websocket_manager import IWsManager
from src.domain.game.board import Board
from src.domain.game.die import Die
from src.domain.game.game import Game
from src.domain.game.game_state import GameState
from src.domain.game.i_game_facade import IGameWebSocketFacade
from src.domain.game.player import Player
from src.repositories.auth.auth_repository import AuthRepository


class GameFacadeImpl(IGameWebSocketFacade):
    ws_manager: IWsManager
    repo: AuthRepository

u

    def select_player_start(self, game: Game) -> Player:
        """Select witch player will start the game"""
        players_order = [game.p1, game.p2]
        return choice(players_order)

    def new_game(self, game_id: str) -> Game:
        # Create All the Assets for a new game
        return Game(id=game_id)

    def new_player(self, user: User | None = None) -> Player:
        """Create a new player"""
        board1 = Board()
        die1 = Die()
        return Player(board=board1, die=die1, user=user)

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
        """Return the game id"""
        return self.ws_manager.get_game(game_id)

    def get_winner_player(self, game_id: str) -> None:
        """Get the winner of the game. The player that have more points win the game. If the match
        have a draw the p2 have the victory."""
        game = self.ws_manager.get_game(game_id)
        p1 = game.p1
        p2 = game.p2
        game.winner_player = p1 if p1.board.total_score > p2.board.total_score else p2

    def exist_game(self, game_id: str) -> bool:
        """Check if a game already exist"""
        game = self.ws_manager.get_game(game_id)
        return isinstance(game, Game)

    async def create_or_join_game(self, game_id: str, user_id: str, websocket: WebSocket) -> tuple[Game, Player]:
        """Create a game or Join player to existing game"""
        game = self.get_game(game_id)
        if not self.exist_game(game_id):
            # Create new game
            game = self.new_game(game_id)
            await self.ws_manager.connect(game_id, game, websocket)
            # Create Player 1
            user = self.create_user(user_id)
            player = self.new_player(user)
            self.join_waiting_room(game_id, player)
            message = 'Player 1 Connected'
            await self.update_game(game_id, message)
        else:
            # Create player 2
            user = self.create_user(user_id)
            player = self.new_player(user)
            if not self.is_full_room(game_id):
                self.join_waiting_room(game_id, player)
                # Select Player Start Order
                start_player = self.select_player_start(game)
                game.set_current_player(start_player)
                await self.ws_manager.connect(game_id, game, websocket)
                message = 'Player 2 Connected'
                self.update_game_state(game, GameState.ROLL_DICE)
                await self.update_game(game_id, message)
        return game, ic(player)

    def create_user(self, user_id) -> User:
        # Add User Initial Values
        user = self.repo.get_user_by_id(user_id)
        user.user_level = self.repo.get_user_level(user.user_id)
        user.bank_account = self.repo.get_user_bank_account(user.user_id)
        return user

    async def update_game(self, game_id: str, message: str) -> None:
        """Update the match board"""
        await self.ws_manager.send_match(game_id, message)

    def update_game_state(self, game: Game, new_state: GameState) -> None:
        """Update the state of the game"""
        if game.state != new_state:
            game.state = new_state

    async def get_player_event_message(self, websocket: WebSocket) -> str:
        """This receives the players events from the client. This Json have the key 'message'.
        From this key you will extract the event message."""
        import json
        response = await websocket.receive()
        text_dict = response.get('text')
        json_data = json.loads(text_dict)
        return json_data.get('message')

    def get_remained_player_websocket(self, game_id: str) -> WebSocket:
        """Return the Remained player. This is useful after a user disconnect from the match"""
        active_connection = self.ws_manager.active_connection.get(game_id)
        if active_connection:
            return list(active_connection)[0]

    async def get_winner_after_player_disconnect(self, player: Player, game: Game, game_id: str, websocket: WebSocket):
        await self.ws_manager.disconnect(game_id, websocket)
        room_websockets = self.ws_manager.active_connection.get(game_id)
        if room_websockets:
            remaining_player_websocket = list(room_websockets)[0]
            opponent_player = game.p1 if player.id != game.p1.id else game.p2
            game.winner_player = opponent_player
            await remaining_player_websocket.send_json(
                {'match': game.model_dump_json(), 'status': 'player disconnected'})
