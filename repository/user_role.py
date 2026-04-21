from enum import StrEnum
from typing import Optional

from tortoise.expressions import Q

from database.tables import Role, User
from model.role import RoleSchema
from model.user import UserSchema
from model.user_role import UserWithRoleSchema

class ErrorEnum(StrEnum):
    LOGIN_NOT_FOUND = "login_not_found"
    ROLE_NOT_FOUND = "role_not_found"


class UserRoleRepository:
    async def bind_role_to_user(self, login: str, role_name: str) -> UserWithRoleSchema | ErrorEnum:
        user = await User().get_or_none(Q(email=login) | Q(username=login)).prefetch_related("roles")
        if user:
            role = await Role().get_or_none(role_name=role_name)
            if role:
                await user.roles.add(role)
            else:
                return ErrorEnum.ROLE_NOT_FOUND
            return await self.__save_changes_and_get_pydantic_model(user)
        else:
            return ErrorEnum.LOGIN_NOT_FOUND

    async def unbind_role_from_user(self, login: str, role_name: str) -> UserWithRoleSchema | ErrorEnum:
        user = await User().get_or_none(Q(email=login) | Q(username=login)).prefetch_related("roles")
        if user:
            role = await Role().get_or_none(role_name=role_name)
            if role:
                await user.roles.remove(role)
            else:
                return ErrorEnum.ROLE_NOT_FOUND
        else:
            return ErrorEnum.LOGIN_NOT_FOUND
        return await self.__save_changes_and_get_pydantic_model(user)

    @staticmethod
    async def __save_changes_and_get_pydantic_model(user: User) -> UserWithRoleSchema:
        await user.save()
        roles = await user.roles.all()
        roles_pydantic = [RoleSchema(id=role.pk, role_name=role.role_name) for role in roles]
        return UserWithRoleSchema(
            user_schema=UserSchema(
                id=user.pk,
                username=user.username,
                email=user.email,
                password_hash=user.password_hash,
                token_version=user.token_version
            ),
            roles=roles_pydantic
        )

    @staticmethod
    async def get_user_with_roles(login: str) -> Optional[UserWithRoleSchema]:
        user = await User().get_or_none(Q(email=login) | Q(username=login)).prefetch_related("roles")
        roles: list[Role] = await user.roles.all()
        roles_pydantic: list[RoleSchema] = []

        for role in roles:
            role_orm = await Role().get(Q(id=role.pk))
            roles_pydantic.append(RoleSchema(id=role_orm.pk, role_name=role_orm.role_name))

        if user:
            return UserWithRoleSchema(
                user_schema=UserSchema(
                    id=user.pk,
                    username=user.username,
                    email=user.email,
                    password_hash=user.password_hash,
                    token_version=user.token_version
                ),
                roles=roles_pydantic
            )
        else:
            return None

    @staticmethod
    async def get_roles_by_login(login: str) -> list[RoleSchema] | list | None:
        user = await User().get_or_none(Q(email=login) | Q(username=login)).prefetch_related("roles")
        if user:
            roles: list[Role] = await user.roles.all()
            if roles:
                return [RoleSchema(id=role.pk, role_name=role.role_name) for role in roles]
            else:
                return []
        else:
            return None

    @staticmethod
    async def all_with_roles() -> list[UserWithRoleSchema]:
        users = await User().all().prefetch_related("roles")
        users_with_roles = []
        for user in users:
            roles: list[Role] = await user.roles.all()
            users_with_roles.append(
                UserWithRoleSchema(
                    user_schema=UserSchema(
                        id=user.pk,
                        username=user.username,
                        email=user.email,
                        password_hash=user.password_hash,
                        token_version=user.token_version,
                    ),
                    roles=[RoleSchema(id=role.pk, role_name=role.role_name) for role in roles]
                )
            )
        return users_with_roles