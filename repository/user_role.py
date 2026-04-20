from typing import Optional

from core.repository.repository import BaseDbRepository, DtoType


class UserRoleRepository(BaseDbRepository):
    async def create(self, *args, **kwargs) -> DtoType:
        pass

    async def get_by_id(self, *args, **kwargs) -> Optional[DtoType]:
        pass

    async def get_all(self) -> list[DtoType]:
        pass

    async def update_by_id(self, *args, **kwargs) -> Optional[DtoType]:
        pass

    async def delete_by_id(self, *args, **kwargs) -> bool:
        pass

    async def delete_all(self) -> bool:
        pass

    async def id_exists(self, *args, **kwargs) -> bool:
        pass