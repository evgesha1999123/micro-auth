from typing import TypeVar, Optional

from pydantic import BaseModel

from model.user import UserSchema, UserRegistrationSchema, UserLoginSchema
from model.user_role import UserWithRoleSchema
from service.exceptions import PasswordVerificationFailed
from service.user import UserService
from service.user_role import UserRoleService
from utils.password_utils import PasswordUtil

T = TypeVar('T', bound=BaseModel)

class AuthService:
    DEFAULT_ROLE = "user"

    def __init__(
            self,
            user_service: UserService,
            user_role_service: UserRoleService,
            password_util: PasswordUtil
    ) -> None:
        self.user_service = user_service
        self.user_role_service = user_role_service
        self.password_util = password_util

    async def register(self, registration_schema: UserRegistrationSchema) -> UserSchema | None:
        user = await self.user_service.add_user(registration_schema)
        if user:
            user_with_role = await self.user_role_service.bind_role_to_user(user.username, self.DEFAULT_ROLE)
            return user_with_role.user_schema
        else:
            return None

    async def login(self, login_schema: UserLoginSchema) -> Optional[UserWithRoleSchema]:
        user = await self.user_service.get_user(login_schema.login)
        if user:
            if self.password_util.verify_password(login_schema.password, user.password_hash):
                return await self.user_role_service.get_with_roles(login_schema.login)
            else:
                raise PasswordVerificationFailed(login=login_schema.login)
        else:
            return None

    async def logout(self, username: str) -> bool:
        pass