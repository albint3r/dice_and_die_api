class PlayerError(Exception):
    """Base Class Board Errors"""


class InvalidNewBoard(PlayerError):
    """Throw if the Board is not new. This means the columns are empty"""


class InvalidNewDie(PlayerError):
    """Throw if the Die is not new. These means have an integer value"""
