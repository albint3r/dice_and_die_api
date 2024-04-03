from pydantic import BaseModel, EmailStr, SecretStr, Field


class RequestAuthEmail(BaseModel):
    email: EmailStr = Field(exclude=True)
    password: SecretStr = Field(exclude=True, min_length=9)


class RequestNameAndLastName(BaseModel):
    """Schema SignIn Responses"""
    name: str
    last_name: str
