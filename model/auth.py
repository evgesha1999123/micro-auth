from typing import Optional

from pydantic import BaseModel, Field


class UserRegistrationSchema(BaseModel):
    username: str
    email: Optional[str] = None
    password: str

class UserLoginSchema(BaseModel):
    login: str
    password: str

class LoginResponseSchema(BaseModel):
    access_token: str = Field(..., description="User access token")
    refresh_token: Optional[str] = Field(default=None, description="User refresh token")
    message: Optional[str] = Field(default="User authentication successful", description="Login response message")

class LogoutResponseSchema(BaseModel):
    message: Optional[str] = Field(default="User logout successful", description="Logout response message")