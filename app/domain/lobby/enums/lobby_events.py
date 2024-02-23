from enum import Enum


class LobbyEvents(Enum):
    INVALID_INPUT_EVENT: str = 'invalid_input_event'
    UPDATE_GAMES: str = 'update_games'
