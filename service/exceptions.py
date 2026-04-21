from pydantic import BaseModel

from core.service.exception import BaseCustomRecordException
from typing import TypeVar

T = TypeVar('T', bound=BaseModel)

class PasswordVerificationFailed(BaseCustomRecordException):
    def __init__(self, login: str) -> None:
        message = f"Wrong password for user '{login}'!"
        super().__init__(message)


class UsernameAlreadyExists(BaseCustomRecordException):
    def __init__(self, username: str) -> None:
        message = f"Username '{username}' already exists!"
        super().__init__(message)


class EmailAlreadyExists(BaseCustomRecordException):
    def __init__(self, email: str) -> None:
        message = f"Email '{email}' already exists!"
        super().__init__(message)