from abc import ABC


class GameError(Exception, ABC):
    """This is the Base Error"""


class RemoveValuesFromColumnError(GameError):
    """Throw this error when the Column can't remove more values"""


class AddValuesFromColumnError(GameError):
    """Throw this error when the Column can't Add more values"""


class InvalidNewBoardInstance(GameError):
    """Throw this error when the Board is not a new one"""


class InvalidNewDieInstance(GameError):
    """Throw this error when the Die is not a new one"""


class NotRemainingActiveConnectionsErro(GameError):
    """Throw this error when try to get the remaining connections and are empty"""
