import uuid
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ReferralProgram(BaseModel):
    creation_date: datetime = Field(default=datetime.now)
    referral_code: UUID = Field(default_factory=uuid.uuid4)
    promoter_user_id: UUID | None
    referred_user_id: UUID | None
    total_deposits: int = 0
    total_rewards: float = 0
    active: bool = True
