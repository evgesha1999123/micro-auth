from typing import Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: Optional[int] = None
    username: str
    email: Optional[str] = None
    password_hash: str
    token_version: int


class UserRegistrationSchema(BaseModel):
    username: str
    email: Optional[str] = None
    password: str


class UserLoginSchema(BaseModel):
    login: str
    password: str