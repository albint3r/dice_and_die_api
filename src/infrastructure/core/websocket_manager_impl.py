from icecream import ic
from starlette.websockets import WebSocket

from src.domain.core.i_websocket_manager import IWsManager, TMessagePayload, TActiveGamesConnections, TActiveMatches
from src.domain.game.game import Game


class _WsManagerImpl(IWsManager):
    _active_games: TActiveGamesConnections = {}
    _active_match: TActiveMatches = {}

    @property
    def active_connection(self) -> TActiveGamesConnections:
        return self._active_games

    @property
    def active_matches(self) -> TActiveMatches:
        """Get the Websocket active connections"""
        return self._active_match

    def get_match(self, game_id: str) -> Game:
        """Return the Game in the active room"""
        return self._active_match.get(game_id)

    def _create_new_match(self, game_id: str, game: Game, ) -> None:
        """Create a new match"""
        self._active_match.setdefault(game_id, game)

    async def connect(self, game_id: str, game: Game, ws: WebSocket):
        """Connect with a game and match if it not exists."""
        match = self._active_match.get(game_id)
        # If not match create a new One
        if not match:
            self._create_new_match(game_id, game)
        # Add New user to game pool
        self._active_games.setdefault(game_id, set()).add(ws)

    async def disconnect(self, game_id: str, ws: WebSocket):
        self._active_games[game_id].remove(ws)

    async def send_message(self, game_id: str, message: TMessagePayload):
        """Recibe message"""
        game = self._active_games.get(game_id, [])
        match = self.get_match(game_id)
        for ws in game:
            result = {'match': match.model_dump_json()}
            await ws.send_json(result)


ws_manager = _WsManagerImpl()
