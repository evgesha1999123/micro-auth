from typing import Optional

from pydantic import BaseModel

from model.role import RoleSchema


class UserSchema(BaseModel):
    pk: int
    username: str
    email: Optional[str] = None
    password_hash: str
    token_version: int


class UserWithRoleSchema(BaseModel):
    user_schema: UserSchema
    roles: list[RoleSchema]


class UserRegistrationSchema(BaseModel):
    username: str
    email: Optional[str] = None
    password: str


class UserLoginSchema(BaseModel):
    login: str
    password: str