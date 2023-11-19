class BoarError(Exception):
    """Base Class Board Errors"""


class AddError(BoarError):
    """Throw this error when the board cant add more values"""


class RemoveError(BoarError):
    """Throw this error when the board cant remove more values"""


class InvalidColumnError(BoarError):
    """Throw error if is an invalid index column"""
