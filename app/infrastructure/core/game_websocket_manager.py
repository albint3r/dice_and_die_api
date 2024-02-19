from starlette.websockets import WebSocket

from app.domain.core.i_game_websocket_manager import IGameWebSocketManager
from app.domain.core.ref_types import TExtras
from app.domain.game.entities.game import Game
from app.domain.game.errors.errors import NotRemainingActiveConnectionsErro
from app.domain.game.schemas.response import GameResponse


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
        for user_connection in connections:
            response = GameResponse(game=game, message=message, extras=extras)
            await user_connection.send_json(response.model_dump_json())

    def get_remained_player_websocket(self, game_id: str) -> WebSocket:
        connections = self.active_connections.get(game_id)
        if connections:
            websockets = list(connections)[0]
            return websockets
        raise NotRemainingActiveConnectionsErro('Not remaining active connections.')


game_websocket_manger = _GameWebSocketManager()
