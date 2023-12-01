from starlette.websockets import WebSocket

from src.domain.core.i_websocket_manager import IWsManager, TMessagePayload, TActiveGamesConnections, TActiveMatches
from src.domain.game.game import Game


class _WsManagerImpl(IWsManager):
    _active_connections: TActiveGamesConnections = {}
    _active_games: TActiveMatches = {}

    @property
    def active_connection(self) -> TActiveGamesConnections:
        return self._active_connections

    @property
    def active_games(self) -> TActiveMatches:
        """Get the Websocket active connections"""
        return self._active_games

    def get_game(self, game_id: str) -> Game:
        """Return the Game in the active room"""
        return self._active_games.get(game_id)

    def _create_new_match(self, game_id: str, game: Game, ) -> None:
        """Create a new match"""
        self._active_games.setdefault(game_id, game)

    async def connect(self, game_id: str, game: Game, ws: WebSocket):
        """Connect with a game and match if it not exists."""
        match = self._active_games.get(game_id)
        # If not match create a new One
        if not match:
            self._create_new_match(game_id, game)
        # Add New user to game pool
        self._active_connections.setdefault(game_id, set()).add(ws)

    async def disconnect(self, game_id: str, ws: WebSocket):
        """Disconnect player from the room. Remove the game if one of the players left the match.
        This have a conditional, because the remaining player could trigger this event, this check
        if the game already exist to be eliminated.
        """
        self._active_connections[game_id].remove(ws)
        if self.active_games.get(game_id):
            del self._active_games[game_id]

    async def send_message(self, game_id: str, message: TMessagePayload):
        """Send Json message with the key Status to the listeners users"""
        game = self._active_connections.get(game_id, {})
        for ws in game:
            result = {'status': message}
            await ws.send_json(result)

    async def send_match(self, game_id: str, message: str | None = None):
        """Send the Current Json Match to all the listeners in the game"""
        game = self._active_connections.get(game_id, {})
        match = self.get_game(game_id)
        for ws in game:
            result = {'match': match.model_dump_json(), 'status': message if message else ''}
            await ws.send_json(result)

    def get_remained_player_websocket(self, game_id: str) -> WebSocket:
        """Return the Remained player. This is useful after a user disconnect from the match"""
        active_connection = self.ws_manager.active_connection.get(game_id)
        if active_connection:
            return list(active_connection)[0]

    def is_game_full(self, game_id: str) -> bool:
        """Check if Is full the game room"""
        game = self._active_connections.get(game_id, [])
        return len(game) == 2


ws_manager = _WsManagerImpl()
