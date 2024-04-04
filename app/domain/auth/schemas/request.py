from pydantic import BaseModel, EmailStr, SecretStr, Field


class LoginOrSignInRequest(BaseModel):
    email: EmailStr = Field(exclude=True)
    password: SecretStr = Field(exclude=True, min_length=8)


class UserUpdateNamesRequest(BaseModel):
    """Schema SignIn Responses"""
    name: str
    last_name: str
