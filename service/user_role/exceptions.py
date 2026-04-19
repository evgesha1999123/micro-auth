from database.tables import User


class BaseUserAuthorizationException(Exception):
    def __init__(self, user: User, *args: tuple) -> None:
        self.user = user
        self.args = args


class UserAlreadyExistsException(BaseUserAuthorizationException):
    def __str__(self) -> str:
        return f"{self.user} already exists!"


class LoginAlreadyExists(BaseUserAuthorizationException):
    def __str__(self) -> str:
        return f"Login {self.args[0]} for user {self.user} already exists!"