from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import TypeVar, Generic, Optional, Type

DtoType = TypeVar("DtoType", bound=BaseModel)
DbType = TypeVar("DbType")


class BaseDbService(ABC, Generic[DtoType, DbType]):
    def __init__(self, dto_class: Type[DtoType], db_class: Type[DbType]):
        self.dto_class = dto_class
        self.db_class = db_class

    @abstractmethod
    async def create(self, params: DtoType) -> DtoType:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id(self, params: DtoType) -> Optional[DtoType]:
        raise NotImplementedError()

    @abstractmethod
    async def get_all(self) -> list[DtoType]:
        raise NotImplementedError()

    @abstractmethod
    async def update_by_id(self, old_params: DtoType, new_params: DtoType) -> Optional[DtoType]:
        raise NotImplementedError()

    @abstractmethod
    async def delete_by_id(self, params: DtoType) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def delete_all(self) -> bool:
        raise NotImplementedError()