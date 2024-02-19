from pydantic import BaseModel, EmailStr, SecretStr, Field


class RequestAuthEmail(BaseModel):
    email: EmailStr = Field(exclude=True)
    password: SecretStr = Field(exclude=True)
