from database.tables import Role
from model.role import RoleSchema
from service.exceptions.base import RecordAlreadyExistsException


class RoleService:
    @staticmethod
    async def create_role(role_name: str) -> RoleSchema:
        role, created = await Role.get_or_create(role_name=role_name)
        if not created:
            raise RecordAlreadyExistsException(role)
        return RoleSchema(id=role.pk, role_name=role.role_name)

    @staticmethod
    async def get_by_id(id_: int) -> RoleSchema:
        role = await Role().get(id=id_)
        return RoleSchema(id=role.pk, role_name=role.role_name)

    @staticmethod
    async def get_by_name(name: str) -> RoleSchema:
        role = await Role().get(role_name=name)
        return RoleSchema(id=role.pk, role_name=role.role_name)

    @staticmethod
    async def change_role_name_by_id(id_: int, new_name: str) -> RoleSchema:
        role = await Role.get(id=id_)
        role.role_name = new_name
        await role.save()
        return RoleSchema(id=role.pk, role_name=role.role_name)

    @staticmethod
    async def change_role_name_by_name(old_name: str, new_name: str) -> RoleSchema:
        role = await Role().get(role_name=old_name)
        role.role_name = new_name
        await role.save()
        return RoleSchema(id=role.pk, role_name=role.role_name)

    @staticmethod
    async def delete_role(id_: int) -> bool:
        role = await Role().get(id=id_)
        await role.delete()
        role = await role.get_or_none(id=id_)
        deleted = not bool(role)
        return deleted

    @staticmethod
    async def get_all() -> list[RoleSchema]:
        roles = await Role().all()
        return [RoleSchema(id=role.pk, role_name=role.role_name) for role in roles]