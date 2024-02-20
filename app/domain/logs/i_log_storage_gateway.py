from pydantic import BaseModel
from abc import ABC, abstractmethod


class ILogStorageGateWay(BaseModel, ABC):
    """This is an interface to save the error logs in a storage"""

    @abstractmethod
    def store_log_msg(self, *args, **kwargs) -> None:
        """This method save the error message from the logger"""
