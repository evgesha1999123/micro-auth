from typing import TypeVar
import tortoise

T = TypeVar('T', bound=tortoise.Model)

class BaseCustomRecordException(Exception):
    def __init__(self, record: T, *args: tuple) -> None:
        self.record = record
        self.args = args


class RecordAlreadyExistsException(BaseCustomRecordException):
    def __str__(self) -> str:
        return f"{self.record} already exists!"