from pydantic import BaseModel

from model.role import RoleSchema
from model.user import UserSchema


class UserWithRoleSchema(BaseModel):
    user_schema: UserSchema
    roles: list[RoleSchema]