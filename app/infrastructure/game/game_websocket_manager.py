from typing import Final

from starlette.websockets import WebSocket

from app.domain.core.ref_types import TExtras
from app.domain.game.entities.game import Game
from app.domain.game.errors.errors import NotRemainingActiveConnectionsError, MissingBroadcastGameInPlayersMatch
from app.domain.game.schemas.response import ResponseGame
from app.domain.game.use_cases.i_game_websocket_manager import IGameWebSocketManager


class _GameWebSocketManager(IGameWebSocketManager):

    async def connect(self, game_id: str, new_game: Game, websocket: WebSocket) -> None:
        await websocket.accept()
        game = self.active_games.get(game_id)
        # Create a new game if not exist.
        if not game:
            self.active_games.setdefault(game_id, new_game)
        # Add user to game pool connections
        self.active_connections.setdefault(game_id, set()).add(websocket)

    async def disconnect(self, game_id: str, websocket: WebSocket) -> None:
        if game_id in self.active_connections:
            # Eliminar el websocket desconectado del conjunto de conexiones activas
            self.active_connections[game_id].remove(websocket)
            # Verificar si el conjunto está vacío después de eliminar el websocket
            if not self.active_connections[game_id]:
                # Si el conjunto está vacío, eliminar la entrada del juego activo
                del self.active_connections[game_id]
                # También eliminar la entrada del juego activo si existe en el diccionario de juegos activos
                if self.active_games.get(game_id):
                    del self.active_games[game_id]

    async def broadcast(self, game_id: str, message: str = '', extras: TExtras | None = None) -> None:
        connections = self.active_connections.get(game_id, {})
        game = self.active_games.get(game_id)
        if not game:
            raise MissingBroadcastGameInPlayersMatch("You cant' broadcast to players if Game not longer exist. "
                                                     f"Most probably the game with id: {game_id} is finished and your "
                                                     "are trying to send message to a ended game.")

        response = ResponseGame(game=game, message=message, extras=extras)
        jsons_response = response.model_dump_json()
        for user_connection in connections:
            await user_connection.send_json(jsons_response)

    def get_remained_player_websocket(self, game_id: str) -> WebSocket:
        connections = self.active_connections.get(game_id)
        if connections:
            websockets = list(connections)[0]
            return websockets
        raise NotRemainingActiveConnectionsError('Not remaining active connections.')

    def is_full(self, game_id: str) -> bool:
        game = self.active_connections.get(game_id)
        if game:
            return len(game) == 2
        return False


game_websocket_manger: Final[IGameWebSocketManager] = _GameWebSocketManager()
