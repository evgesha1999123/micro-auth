from core.service.exception import RecordAlreadyExistsException, RecordDoesNotExistsException
from model.role import RoleSchema
from repository.role import RoleDbRepository
import logging

logger = logging.getLogger(__name__)


class RoleService:
    def __init__(self, role_repo: RoleDbRepository):
        self.repo = role_repo


    async def create_role(self, name: str) -> RoleSchema:
        logger.info(f"[{self.__class__.__name__}] Create role request: name='{name}'")

        role_schema, created = await self.repo.create(name)

        if created:
            logger.info(f"[{self.__class__.__name__}] Role created: name='{name}', id={role_schema.id}")
            return role_schema

        logger.warning(f"[{self.__class__.__name__}] Role already exists: name='{name}', id={role_schema.id}")
        raise RecordAlreadyExistsException(role_schema)


    async def get_by_id(self, role_id: int) -> RoleSchema:
        logger.info(f"[{self.__class__.__name__}] Get role by id: {role_id}")

        if await self.repo.id_exists(role_id):
            role = await self.repo.get_by_id(role_id)
            logger.info(f"[{self.__class__.__name__}] Role found: id={role_id}")
            return role

        logger.warning(f"[{self.__class__.__name__}] Role not found by id: {role_id}")
        raise RecordDoesNotExistsException(id=role_id)


    async def get_by_name(self, name: str) -> RoleSchema:
        logger.info(f"[{self.__class__.__name__}] Get role by name: '{name}'")

        if await self.repo.role_name_exists(name):
            role = await self.repo.get_by_name(name)
            logger.info(f"[{self.__class__.__name__}] Role found: name='{name}'")
            return role

        logger.warning(f"[{self.__class__.__name__}] Role not found by name: '{name}'")
        raise RecordDoesNotExistsException(name=name)


    async def change_name_by_id(self, id_: int, name: str) -> RoleSchema:
        logger.info(f"[{self.__class__.__name__}] Change role name by id: id={id_} -> '{name}'")

        if await self.repo.id_exists(id_):
            if not await self.repo.role_name_exists(name):
                role = await self.repo.update_by_id(id_, name)
                logger.info(f"[{self.__class__.__name__}] Role updated: id={id_}, new_name='{name}'")
                return role

            logger.warning(f"[{self.__class__.__name__}] Cannot update role: id={id_}, name='{name}'")
            raise RecordAlreadyExistsException(await self.repo.get_by_name(name))

        logger.warning(f"[{self.__class__.__name__}] Cannot update role: id={id_}, name='{name}'")
        raise RecordDoesNotExistsException(id=id_)


    async def change_name_by_old_name(self, old_name: str, new_name: str) -> RoleSchema:
        logger.info(f"[{self.__class__.__name__}] Change role name: '{old_name}' -> '{new_name}'")

        if await self.repo.role_name_exists(old_name):
            if not await self.repo.role_name_exists(new_name):
                role = await self.repo.update_by_name(old_name, new_name)
                logger.info(f"[{self.__class__.__name__}] Role updated: '{old_name}' -> '{new_name}'")
                return role

            logger.warning(f"[{self.__class__.__name__}] Cannot update role: '{old_name}' -> '{new_name}'")
            raise RecordAlreadyExistsException(await self.repo.get_by_name(old_name))

        logger.warning(f"[{self.__class__.__name__}] Cannot update role: name='{old_name}' not found!")
        raise RecordDoesNotExistsException(role_name=old_name)


    async def delete_by_id(self, id_: int) -> bool:
        logger.info(f"[{self.__class__.__name__}] Delete role by id: {id_}")

        if await self.repo.id_exists(id_):
            result = await self.repo.delete_by_id(id_)
            logger.info(f"[{self.__class__.__name__}] Role deleted: id={id_}")
            return result

        logger.warning(f"[{self.__class__.__name__}] Role not found for deletion: id={id_}")
        raise RecordDoesNotExistsException(id=id_)


    async def delete_by_name(self, name: str) -> bool:
        logger.info(f"[{self.__class__.__name__}] Delete role by name: '{name}'")

        if await self.repo.role_name_exists(name):
            result = await self.repo.delete_by_name(name)
            logger.info(f"[{self.__class__.__name__}] Role deleted: name='{name}'")
            return result

        logger.warning(f"[{self.__class__.__name__}] Role not found for deletion: name='{name}'")
        raise RecordDoesNotExistsException(role_name=name)


    async def get_all(self) -> list[RoleSchema]:
        logger.info(f"[{self.__class__.__name__}] Get all roles")

        roles = await self.repo.get_all()

        logger.info(f"[{self.__class__.__name__}] Roles fetched: count={len(roles)}")
        return roles


    async def delete_all(self) -> bool:
        logger.warning(f"[{self.__class__.__name__}] Delete ALL roles request")

        result = await self.repo.delete_all()

        logger.warning(f"[{self.__class__.__name__}] All roles deleted")
        return result