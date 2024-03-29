from datetime import datetime
from typing import Any

from starlette.websockets import WebSocket

from app.domain.game.entities.game import Game
from app.domain.game.entities.player import Player

"""This file have all the type in the app"""

TCurrentScore: dict[int, int]
TActiveConnections = dict[str, set[WebSocket]]
TActiveConnectionsViewers = dict[str, set[WebSocket]]
TActiveGames = dict[str, Game]
TLobbyActiveConnections = dict[str, dict[WebSocket, datetime]]
TExtras = dict[str, Any]
TGamePlayer = tuple[Game, Player]
