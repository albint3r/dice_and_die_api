from pydantic import BaseModel, EmailStr, SecretStr, Field


class LoginRequest(BaseModel):
    email: EmailStr = Field(exclude=True)
    password: SecretStr = Field(exclude=True, min_length=8)


class SignInRequest(BaseModel):
    email: EmailStr = Field(exclude=True)
    name: str = Field(min_length=4, max_length=30, default='')
    password: SecretStr = Field(exclude=True, min_length=8)
    referral_code: str | None = None


class LogInWithGoogle(BaseModel):
    google_user_id: str


class UserUpdateNamesRequest(BaseModel):
    """Schema SignIn Responses"""
    name: str
    last_name: str
