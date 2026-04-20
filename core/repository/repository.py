from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import TypeVar, Generic, Optional, Type

DtoType = TypeVar("DtoType", bound=BaseModel)
DbType = TypeVar("DbType")


class BaseDbRepository(ABC, Generic[DtoType, DbType]):
    def __init__(self, dto_class: Type[DtoType], db_class: Type[DbType]):
        self.dto_class = dto_class
        self.db_class = db_class

    @abstractmethod
    async def create(self, *args, **kwargs) -> DtoType:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id(self, *args, **kwargs) -> Optional[DtoType]:
        raise NotImplementedError()

    @abstractmethod
    async def get_all(self) -> list[DtoType]:
        raise NotImplementedError()

    @abstractmethod
    async def update_by_id(self, *args, **kwargs) -> Optional[DtoType]:
        raise NotImplementedError()

    @abstractmethod
    async def delete_by_id(self, *args, **kwargs) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def delete_all(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def id_exists(self, *args, **kwargs) -> bool:
        raise NotImplementedError()