from abc import ABC


class AuthErrors(Exception, ABC):
    """This is the base Auth Error class"""


class UserLevelNotExist(AuthErrors):
    """User ID don't match with the table UserLevel"""


class ErrorValidationNotPositiveAmount(AuthErrors):
    """Error validation to check if the amount is positive"""


class NoUserInRanking(AuthErrors):
    """Raise this error when the ranking ladder is empty"""
