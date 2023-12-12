from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from src.domain.auth.errors import ErrorValidationNotPositiveAmount


class BankAccount(BaseModel):
    creation_date: datetime = Field(exclude=True)
    bank_account_id: str = Field(exclude=True)
    user_id: str = Field(exclude=True)
    amount: float = 0.0

    @field_validator('amount')
    def validate_positive_amount(cls, amount: float):
        if amount >= 0:
            return amount
        raise ErrorValidationNotPositiveAmount('The amount must be positive: 0.0')
