from pydantic import BaseModel

from app.domain.referral_program.entities.referral_program import ReferralProgram


class PromoterUserHistoryResponse(BaseModel):
    """Return the Promoter user History of their referrals"""
    referrals: list[ReferralProgram]
