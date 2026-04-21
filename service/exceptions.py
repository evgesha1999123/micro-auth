from pydantic import BaseModel

from core.service.exception import BaseCustomRecordException
from typing import TypeVar

T = TypeVar('T', bound=BaseModel)

class PasswordVerificationFailed(BaseCustomRecordException):
    def __init__(self, username: str) -> None:
        message = f"Wrong password for user '{username}'!"
        super().__init__(message)