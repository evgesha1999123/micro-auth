from typing import TypeVar, Optional

from pydantic import BaseModel

from model.user import UserSchema, UserRegistrationSchema, UserLoginSchema
from repository.user import UserDbRepository

T = TypeVar('T', bound=BaseModel)

class AuthService:
    def __init__(self, user_repo: UserDbRepository) -> None:
        self.user_repo = user_repo

    async def register(self, registration_schema: UserRegistrationSchema) -> UserSchema:
        pass

    async def login(self, login_schema: UserLoginSchema) -> Optional[UserSchema]:
        pass

    async def logout(self, username: str) -> bool:
        pass