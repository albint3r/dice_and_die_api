from abc import ABC, abstractmethod

from pydantic import BaseModel

from app.domain.referral_program.entities.referral_program import ReferralProgram
from app.domain.referral_program.schemas.response import PromoterUserHistoryResponse


class IReferralProgramRepository(BaseModel, ABC):

    @abstractmethod
    def can_user_be_referred(self, referred_user_id: str) -> bool:
        """Return TRUE if the user is not already referred by other user."""

    @abstractmethod
    def create_referral_program_from_promoter(self, promoter_user_id: str, referred_user_id: str):
        """This method create the referral promoter for each new user created"""

    @abstractmethod
    def create_referral_transactions(self, referral_code: str, amount: float):
        """Update the information when a user make a deposit"""

    @abstractmethod
    def get_promoter_user_history(self, promoter_user_id: str) -> PromoterUserHistoryResponse:
        """This method create the referral promoter for each new user created"""

    @abstractmethod
    def get_referred_record(self, referred_user_id: str) -> ReferralProgram | None:
        """Get the data of the referred record."""
