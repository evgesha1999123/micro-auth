from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock

from tortoise import Tortoise

from core.di import container
from core.service.exception import (
    RecordAlreadyExistsException,
    RecordDoesNotExistsException,
)
from database.db import TORTOISE_ORM
from database.tables import User
from service.exceptions import PasswordVerificationFailed
from service.user import UserService


class TestUserService(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        await self.__ensure_connection()
        await Tortoise.generate_schemas()
        self.repo = AsyncMock()
        self.password_util = MagicMock()
        self.service = container.get(UserService)

    async def asyncTearDown(self):
        await self.clear()
        await Tortoise.close_connections()

    async def clear(self):
        await User.all().delete()

    @staticmethod
    async def __ensure_connection():
        if not Tortoise._inited:
            await Tortoise.init(config=TORTOISE_ORM)

    # ========== change_username ==========

    async def test_change_username_success(self):
        old_user = MagicMock(id=1, username="old")
        updated_user = MagicMock(id=1, username="new")

        self.repo.get_by_unique_field.side_effect = [old_user, None]
        self.repo.update_by_id.return_value = updated_user

        result = await self.service.change_username("old", "new")

        self.assertEqual(result.username, "new")

    async def test_change_username_old_not_found(self):
        self.repo.get_by_unique_field.return_value = None

        with self.assertRaises(RecordDoesNotExistsException):
            await self.service.change_username("old", "new")

    async def test_change_username_new_already_exists(self):
        old_user = MagicMock(id=1)
        new_user = MagicMock(id=2)

        self.repo.get_by_unique_field.side_effect = [old_user, new_user]

        with self.assertRaises(RecordAlreadyExistsException):
            await self.service.change_username("old", "new")

    # ========== change_password ==========

    async def test_change_password_success(self):
        user = MagicMock(id=1)

        self.service._UserService__get_verified_user = AsyncMock(return_value=user)
        self.password_util.get_password_hash.return_value = "hashed"

        self.repo.update_by_id.return_value = user

        result = await self.service.change_password("user", "old", "new")

        self.assertEqual(result, user)

    async def test_change_password_failed(self):
        self.service._UserService__get_verified_user = AsyncMock(return_value=None)

        with self.assertRaises(PasswordVerificationFailed):
            await self.service.change_password("user", "old", "new")

    # ========== change_email ==========

    async def test_change_email_success(self):
        old_user = MagicMock(id=1, email="old@mail.com")
        updated_user = MagicMock(id=1, email="new@mail.com")

        self.repo.get_by_unique_field.side_effect = [old_user, None]
        self.repo.update_by_id.return_value = updated_user

        result = await self.service.change_email("old@mail.com", "new@mail.com")

        self.assertEqual(result.email, "new@mail.com")

    async def test_change_email_old_not_found(self):
        self.repo.get_by_unique_field.return_value = None

        with self.assertRaises(RecordDoesNotExistsException):
            await self.service.change_email("old@mail.com", "new@mail.com")

    async def test_change_email_new_exists(self):
        old_user = MagicMock(id=1)
        new_user = MagicMock(id=2)

        self.repo.get_by_unique_field.side_effect = [old_user, new_user]

        with self.assertRaises(RecordAlreadyExistsException):
            await self.service.change_email("old@mail.com", "new@mail.com")

    # ========== get_user ==========

    async def test_get_user_success(self):
        user = MagicMock(username="user")
        self.repo.get_by_login.return_value = user

        result = await self.service.get_user("user")

        self.assertEqual(result.username, "user")

    async def test_get_user_not_found(self):
        self.repo.get_by_login.return_value = None

        with self.assertRaises(RecordDoesNotExistsException):
            await self.service.get_user("user")

    # ========== delete_user ==========

    async def test_delete_user_success(self):
        self.repo.id_exists.return_value = True
        self.repo.delete_by_id.return_value = True

        result = await self.service.delete_user(1)

        self.assertTrue(result)

    async def test_delete_user_not_found(self):
        self.repo.id_exists.return_value = False

        with self.assertRaises(RecordDoesNotExistsException):
            await self.service.delete_user(1)

    # ========== get_all ==========

    async def test_get_all(self):
        users = [MagicMock(), MagicMock()]
        self.repo.get_all.return_value = users

        result = await self.service.get_all()

        self.assertEqual(len(result), 2)