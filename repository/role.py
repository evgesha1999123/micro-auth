from database.tables import Role
from model.role import RoleSchema
from core.repository.repository import BaseDbRepository


class RoleDbRepository(BaseDbRepository[RoleSchema, Role]):
    async def id_exists(self, id_: int) -> bool:
        record = await self.db_class().get_or_none(id=id_)
        return bool(record)

    async def role_name_exists(self, role_name: str) -> bool:
        record = await self.db_class().get_or_none(role_name=role_name)
        return bool(record)

    async def create(self, role_name: str) -> tuple[RoleSchema, bool]:
        role, created = await self.db_class().get_or_create(role_name=role_name)
        return self.dto_class(id=role.pk, role_name=role.role_name), created

    async def get_by_id(self, id_: int) -> RoleSchema:
        role = await self.db_class().get(id=id_)
        return self.dto_class(id=role.pk, role_name=role.role_name)

    async def get_by_name(self, name: str) -> RoleSchema:
        role = await self.db_class().get(role_name=name)
        return self.dto_class(id=role.pk, role_name=role.role_name)

    async def get_all(self) -> list[RoleSchema]:
        roles = await self.db_class().all()
        return [self.dto_class(id=role.pk, role_name=role.role_name) for role in roles]

    async def update_by_id(self, id_: int, new_name: str) -> RoleSchema:
        role = await self.db_class.get(id=id_)
        role.role_name = new_name
        await role.save()
        return self.dto_class(id=role.pk, role_name=role.role_name)

    async def update_by_name(self, old_name: str, new_name: str) -> RoleSchema:
        role = await self.db_class.get(role_name=old_name)
        role.role_name = new_name
        await role.save()
        return self.dto_class(id=role.pk, role_name=role.role_name)

    async def delete_by_id(self, id_: int) -> bool:
        role = await self.db_class.get(id=id_)
        await role.delete()
        role = await role.get_or_none(id=id_)
        deleted = not bool(role)
        return deleted

    async def delete_by_name(self, name: str) -> bool:
        role = await self.db_class.get(role_name=name)
        await role.delete()
        role = await role.get_or_none(role_name=name)
        deleted = not bool(role)
        return deleted

    async def delete_all(self) -> bool:
        await self.db_class().all().delete()
        roles = await self.db_class().all()
        is_empty = bool(len(roles) == 0)
        return is_empty