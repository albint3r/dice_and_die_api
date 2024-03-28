from abc import ABC


class AnalyticsError(Exception, ABC):
    """This is the Base Error"""


class NotExistedSinglePlayHistoryRecords(AnalyticsError):
    """Throw this error when you don't find any single record"""
