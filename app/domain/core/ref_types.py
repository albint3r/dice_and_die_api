from typing import Any

from starlette.websockets import WebSocket

from app.domain.game.entities.game import Game

"""This file have all the type in the app"""

TCurrentScore: dict[int, int]
TActiveConnections = dict[str, set[WebSocket]]
TActiveGames = dict[str, Game]
TExtras = dict[str, Any]
