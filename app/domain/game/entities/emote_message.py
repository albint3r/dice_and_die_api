from pydantic import BaseModel

from app.domain.game.enums.emotes import Emote


class EmoteMessage(BaseModel):
    emote: Emote
