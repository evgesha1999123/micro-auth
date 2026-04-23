from enum import StrEnum
from typing import Optional
from fastapi import Response

from model.auth import UserRegistrationSchema, UserLoginSchema, LoginResponseSchema, LogoutResponseSchema
from model.jwt import JwtSub
from model.user import UserSchema
from service.exceptions import PasswordVerificationFailed
from service.user import UserService
from service.user_role import UserRoleService
from utils.jwt_util import JwtUtil
from utils.password_utils import PasswordUtil

class RoleEnum(StrEnum):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'


class AuthService:
    DEFAULT_ROLE = str(RoleEnum.USER.value)
    COOKIE_KEY = "user_access_token"

    def __init__(
            self,
            user_service: UserService,
            user_role_service: UserRoleService,
            password_util: PasswordUtil,
            jwt_util: JwtUtil,
    ) -> None:
        self.user_service = user_service
        self.user_role_service = user_role_service
        self.password_util = password_util
        self.jwt_util = jwt_util

    async def register(self, registration_schema: UserRegistrationSchema) -> UserSchema | None:
        user = await self.user_service.add_user(registration_schema)
        if user:
            user_with_role = await self.user_role_service.bind_role_to_user(user.username, self.DEFAULT_ROLE)
            return user_with_role.user_schema
        else:
            return None

    async def login(self, *, response: Response, login_schema: UserLoginSchema) -> Optional[LoginResponseSchema]:
        user = await self.user_service.get_user(login_schema.login)
        if user:
            if self.password_util.verify_password(login_schema.password, user.password_hash):
                access_token = self.jwt_util.create_access_token(JwtSub(sub=user.id))
                response.set_cookie(key=self.COOKIE_KEY, value=access_token, httponly=True)
                return LoginResponseSchema(access_token=access_token)
            else:
                raise PasswordVerificationFailed(login=login_schema.login)
        else:
            return None

    async def logout(self, response: Response) -> LogoutResponseSchema:
        response.delete_cookie(key=self.COOKIE_KEY)
        return LogoutResponseSchema()