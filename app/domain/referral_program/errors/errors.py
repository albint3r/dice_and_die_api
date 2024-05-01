from abc import ABC


class ReferralProgramErrors(Exception, ABC):
    """This is the base Auth Error class"""


class ReferralProgramCreationError(ReferralProgramErrors):
    """User ID don't match with the table UserLevel"""


class ReferredUserAlreadyExistError(ReferralProgramErrors):
    """User ID don't match with the table UserLevel"""
