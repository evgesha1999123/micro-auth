from typing import Optional

from database.tables import Role
from model.role import RoleSchema
from service.base.base_service import BaseDbService
from service.exceptions.base import RecordAlreadyExistsException


class RoleDbService(BaseDbService[RoleSchema, Role]):
    async def create(self, params: RoleSchema) -> RoleSchema:
        params_dict = params.model_dump()
        params_dict.pop("id")

        role, created = await self.db_class.get_or_create(**params_dict)
        if not created:
            raise RecordAlreadyExistsException(role)
        return self.dto_class(id=role.pk, role_name=role.role_name)

    async def get_by_id(self, params: RoleSchema) -> RoleSchema:
        role = await self.db_class().get(id=params.id)
        return self.dto_class(id=role.pk, role_name=role.role_name)

    async def get_by_name(self, params: RoleSchema) -> RoleSchema:
        role = await self.db_class().get(role_name=params.role_name)
        return self.dto_class(id=role.pk, role_name=role.role_name)

    async def get_all(self) -> list[RoleSchema]:
        roles = await self.db_class().all()
        return [self.dto_class(id=role.pk, role_name=role.role_name) for role in roles]

    async def update_by_id(self, old_params: RoleSchema, new_params: RoleSchema) -> RoleSchema:
        role = await self.db_class.get(id=old_params.id)
        role.role_name = new_params.role_name
        await role.save()
        return self.dto_class(id=role.pk, role_name=role.role_name)

    async def update_by_name(self, old_params: RoleSchema, new_params: RoleSchema) -> RoleSchema:
        role = await self.db_class.get(role_name=old_params.role_name)
        role.role_name = new_params.role_name
        await role.save()
        return self.dto_class(id=role.pk, role_name=role.role_name)

    async def delete_by_id(self, params: RoleSchema) -> bool:
        role = await self.db_class.get(id=params.id)
        await role.delete()
        role = await role.get_or_none(id=params.id)
        deleted = not bool(role)
        return deleted

    async def delete_by_name(self, params: RoleSchema) -> bool:
        role = await self.db_class.get(role_name=params.role_name)
        await role.delete()
        role = await role.get_or_none(role_name=params.role_name)
        deleted = not bool(role)
        return deleted

    async def delete_all(self) -> bool:
        await self.db_class().all().delete()
        roles = await self.db_class().all()
        is_empty = bool(len(roles) == 0)
        return is_empty