class BoarError(Exception):
    """Base Class Board Errors"""


class AddError(BoarError):
    """Throw this error when the board cant add more values"""


class RemoveError(BoarError):
    """Throw this error when the board cant remove more values"""


class InvalidColumnError(BoarError):
    """Throw error if is an invalid index column"""


class PlayerError(Exception):
    """Base Class Board Errors"""


class InvalidNewBoard(PlayerError):
    """Throw if the Board is not new. This means the columns are empty"""


class InvalidNewDie(PlayerError):
    """Throw if the Die is not new. These means have an integer value"""
