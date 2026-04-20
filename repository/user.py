from typing import Optional

from core.repository.repository import BaseDbRepository, DtoType


class UserDbRepository(BaseDbRepository):
    async def id_exists(self, params: DtoType) -> bool:
        pass

    async def create(self, params: DtoType) -> DtoType:
        pass

    async def get_by_id(self, params: DtoType) -> Optional[DtoType]:
        pass

    async def get_all(self) -> list[DtoType]:
        pass

    async def update_by_id(self, old_params: DtoType, new_params: DtoType) -> Optional[DtoType]:
        pass

    async def delete_by_id(self, params: DtoType) -> bool:
        pass

    async def delete_all(self) -> bool:
        pass