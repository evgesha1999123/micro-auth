from typing import TypeVar, Optional
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class BaseCustomRecordException(Exception):
    def __init__(self, message: str, record: Optional[T] = None, **kwargs) -> None:
        self.record = record
        self.kwargs = kwargs
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return self.message


class RecordAlreadyExistsException(BaseCustomRecordException):
    def __init__(self, record: T) -> None:
        message = f"{record} already exists!"
        super().__init__(message, record=record)


class RecordDoesNotExistsException(BaseCustomRecordException):
    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs
        if kwargs:
            params = []
            for key, value in kwargs.items():
                params.append(f"'{key}': {value}")
            message = f"Record with params: {' '.join(params)} does not exists!"
        else:
            message = "Record does not exists!"
        super().__init__(message, **kwargs)