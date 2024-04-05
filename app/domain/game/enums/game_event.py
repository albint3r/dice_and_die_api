from enum import Enum


class GameEvent(Enum):
    INVALID_INPUT_EVENT = 'invalid_input_event'
    ROLL = 'roll'
    EMOTE = 'emote'
    COL1 = '1'
    COL2 = '2'
    COL3 = '3'
    COL4 = '4'
    YES = 'yes'
    NO = 'no'
