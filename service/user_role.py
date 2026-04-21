from core.service.exception import RecordDoesNotExistsException
from model.role import RoleSchema
from model.user_role import UserWithRoleSchema
from repository.user_role import UserRoleRepository, ErrorEnum


class UserRoleService:
    def __init__(self, user_role_repo: UserRoleRepository):
        self.user_role_repo = user_role_repo

    async def bind_role_to_user(self, login: str, role_name: str) -> UserWithRoleSchema:
        response = await self.user_role_repo.bind_role_to_user(login, role_name)
        if isinstance(response, ErrorEnum):
            self.__raise_error(response, login, role_name)
        return response

    async def unbind_role_from_user(self, login: str, role_name: str) -> UserWithRoleSchema:
        response = await self.user_role_repo.unbind_role_from_user(login, role_name)
        if isinstance(response, ErrorEnum):
            self.__raise_error(response, login, role_name)
        return response

    @staticmethod
    def __raise_error(response: ErrorEnum, login: str, role_name: str):
        if response == ErrorEnum.ROLE_NOT_FOUND:
            raise RecordDoesNotExistsException(role_name=role_name)
        if response == ErrorEnum.LOGIN_NOT_FOUND:
            raise RecordDoesNotExistsException(login=login)

    async def get_with_roles(self, login: str) -> UserWithRoleSchema:
        user_with_role = await self.user_role_repo.get_user_with_roles(login)
        if not user_with_role:
            raise RecordDoesNotExistsException(login=login)
        return user_with_role

    async def get_user_roles(self, login: str) -> list[RoleSchema] | list:
        roles = await self.user_role_repo.get_roles_by_login(login)
        if isinstance(roles, list):
            return roles
        else:
            raise RecordDoesNotExistsException(login=login)

    async def get_all_with_roles(self) -> list[UserWithRoleSchema]:
        return await self.user_role_repo.all_with_roles()