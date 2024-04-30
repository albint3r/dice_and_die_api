from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ReferralTransaction(BaseModel):
    transaction_id: UUID
    referral_code: UUID
    referred_user_id: UUID
    amount: float
    transaction_date: datetime = Field(default=datetime.now)
