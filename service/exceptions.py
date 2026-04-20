from core.service.exception import BaseCustomRecordException

class LoginAlreadyExists(BaseCustomRecordException):
    def __str__(self) -> str:
        return f"Login {self.args[0]} for user {self.record} already exists!"