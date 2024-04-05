from abc import ABC


class GameError(Exception, ABC):
    """This is the Base Error"""


class RemoveValuesFromColumnError(GameError):
    """Throw this error when the Column can't remove more values"""


class AddValuesFromColumnError(GameError):
    """Throw this error when the Column can't Add more values"""


class InvalidNewBoardInstance(GameError):
    """Throw this error when the Board is not a new one"""


class PlaHistoryDontMatchColumnsLength(GameError):
    """Throw this error when the Board is not a new one"""


class SinglePlaHistoryDontMatchColumnsLength(GameError):
    """Throw this error when the Board is not a new one"""


class InvalidNewDieInstance(GameError):
    """Throw this error when the Die is not a new one"""


class NotRemainingActiveConnectionsError(GameError):
    """Throw this error when try to get the remaining connections and are empty"""


class NoneGameInResponseValidatorError(GameError):
    """Throw an error if the game response don't have a game instance"""


class MissingBroadcastGameInPlayersMatch(GameError):
    """Throw an error you want to broadcast the game and don't exit"""


class InvalidAIPathModel(GameError):
    """Throw when don't find the AI ml model"""
