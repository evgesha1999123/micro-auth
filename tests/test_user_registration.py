import pytest
from unittest import IsolatedAsyncioTestCase

from tortoise import Tortoise

from database.db import TORTOISE_ORM
from model.user import UserRegistrationSchema
from service.user_role.user_registration import UserRegistrationService

class TestUserRegistrationService(IsolatedAsyncioTestCase):
    async def test_create_user(self):
        await Tortoise.init(config=TORTOISE_ORM)
        service = UserRegistrationService()
        user = await service.register_user(
            user_registration_schema=UserRegistrationSchema(username="user", email="user", password="123")
        )
        assert user is not None
        assert user.username == "user"
        assert user.email == "user"
        assert user.password == "123"


# @pytest.mark.asyncio
# async def test_register_user() -> None:
#     service = UserRegistrationService()
#     user = await service.register_user(user_registration_schema=UserRegistrationSchema(username="user", email="user", password="123"))
#     assert user is not None
#     assert user.username == "user"
#     assert user.email == "user"
#     assert user.password == "123"