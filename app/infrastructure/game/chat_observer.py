from datetime import datetime

from icecream import ic
from pydantic import ValidationError

from app.domain.game.entities.emote_message import EmoteMessage
from app.domain.game.entities.game import Game
from app.domain.game.entities.player import Player
from app.domain.game.enums.emotes import Emote
from app.domain.game.enums.game_event import GameEvent
from app.domain.game.schemas.request import GamePlayerRequest
from app.domain.game.use_cases.i_chat_observer import IChatObserver


class ChatObserver(IChatObserver):
    async def execute(self, emote_msg: EmoteMessage, game: Game, player: Player) -> None:
        """ Execute the events emotes"""
        player_id = player.id
        emote = emote_msg.emote.value
        if not game.is_finished and emote_msg.emote != Emote.INVALID_INPUT_EVENT:
            extras = {"player_id": player_id, "emote": emote, "time": datetime.now()}
            message = 'emote'
            await self.websockets_manager.broadcast(game_id=game.game_id, message=message, extras=extras)
            await self.viewers_websockets_manager.broadcast(game, message=message, extras=extras)

    async def listen_request_event(self, request: GamePlayerRequest, game: Game, player: Player) -> None:
        if request.event == GameEvent.EMOTE:
            try:
                emote_message = EmoteMessage(**request.extras)
                await self.execute(emote_message, game, player)
            except ValidationError:
                emote_message = EmoteMessage(emote=Emote.INVALID_INPUT_EVENT)
                await self.execute(emote_message, game, player)
