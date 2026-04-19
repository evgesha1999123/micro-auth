from tortoise import Tortoise

from database.tables import User
from model.user import UserRegistrationSchema, UserSchema
from service.user_role.exceptions import UserAlreadyExistsException


class UserRegistrationService:
    def __init__(self) -> None:
        self.connection = Tortoise.get_connection("default")

    async def register_user(self, user_registration_schema: UserRegistrationSchema) -> UserSchema:
        user, created = await User.get_or_create(**user_registration_schema.model_dump())
        if created:
            return UserSchema(**user.__dict__)
        if user and not created:
            raise UserAlreadyExistsException(user)