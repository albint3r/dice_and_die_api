from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, SecretStr, field_validator

from app.domain.auth.entities.bank_account import BankAccount
from app.domain.auth.entities.user_level import UserLevel


class User(BaseModel):
    creation_date: datetime
    user_id: str = Field(exclude=True)
    email: EmailStr = Field(exclude=True)
    password: SecretStr = Field(exclude=True)
    name: str
    last_name: str
    is_verify: bool = False
    user_level: UserLevel | None = None
    bank_account: BankAccount | None = None

    @field_validator('name')
    def validate_name_format(cls, name: str):
        if name:
            return name.title()
        return ''

    @field_validator('last_name')
    def validate_last_name_format(cls, last_name: str):
        if last_name:
            return last_name.title()
        return ''

    @property
    def full_name(self) -> str:
        return f"{self.name} {self.last_name}"
