from abc import ABC, abstractmethod

from pydantic import BaseModel


class IReferralProgramUseCase(BaseModel, ABC):

    @abstractmethod
    def create_referral_program_from_promoter(self, promoter_user_id: str, referred_user_id: str):
        """This method create the referral promoter for each new user created"""

    @abstractmethod
    def create_referral_transactions(self, referred_user_id: str):
        """Update the information when a user make a deposit"""

    @abstractmethod
    def get_promoter_user_history(self, promoter_user_id: str):
        """This method create the referral promoter for each new user created"""
