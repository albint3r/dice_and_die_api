from enum import Enum


class GameState(Enum):
    WAITING_PLAYERS: str = "waiting_players"
    ROLL_DICE: str = "roll_dice"
    SELECT_COLUMN: str = "select_column"
    DESTROY_OPPONENT_TARGET_COLUMN: str = "destroy_opponent_target_column"
    ADD_DICE_TO_COLUMN: str = "add_dice_to_column"
    UPDATE_PLAYERS_POINTS: str = "update_players_points"
    FINISH_GAME: str = "finish_game"
    DISCONNECT_PLAYER: str = "disconnect_player"
