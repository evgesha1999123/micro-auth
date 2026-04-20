import unittest
from unittest import IsolatedAsyncioTestCase

from tortoise import Tortoise
from tortoise.exceptions import DoesNotExist

from database.db import TORTOISE_ORM
from database.tables import User
from model.user import UserSchema
from repository.user import UserDbRepository


class TestUserDbRepository(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        await self.__ensure_connection()
        await Tortoise.generate_schemas()
        self.repository = UserDbRepository(
            dto_class=UserSchema,
            db_class=User
        )
        await self.clear()

    async def asyncTearDown(self):
        await self.clear()
        await Tortoise.close_connections()

    @staticmethod
    async def __ensure_connection():
        if not Tortoise._inited:
            await Tortoise.init(config=TORTOISE_ORM)

    async def clear(self):
        await User.all().delete()

    # ========== id_exists ==========

    async def test_id_exists_true(self):
        user = await self.repository.create(
            username="testuser",
            email="test@example.com",
            password_hash="hash123",
            token_version=1
        )
        self.assertTrue(await self.repository.id_exists(user.id))

    async def test_id_exists_false(self):
        self.assertFalse(await self.repository.id_exists(99999))

    # ========== create ==========

    async def test_create_user_success(self):
        user = await self.repository.create(
            username="john_doe",
            email="john@example.com",
            password_hash="secure_hash",
            token_version=1
        )

        self.assertEqual(user.username, "john_doe")
        self.assertEqual(user.email, "john@example.com")
        self.assertEqual(user.password_hash, "secure_hash")
        self.assertEqual(user.token_version, 1)

        db_user = await User.get(username="john_doe")
        self.assertIsNotNone(db_user)
        self.assertEqual(db_user.email, "john@example.com")

    async def test_create_user_without_id(self):
        """Test that id is ignored if passed in kwargs"""
        user = await self.repository.create(
            id=999,
            username="testuser",
            email="test@example.com",
            password_hash="hash",
            token_version=1
        )

        self.assertNotEqual(user.id, 999)
        self.assertEqual(user.username, "testuser")

    # ========== get_by_id ==========

    async def test_get_by_id_success(self):
        created = await self.repository.create(
            username="getuser",
            email="get@example.com",
            password_hash="hash123",
            token_version=1
        )

        fetched = await self.repository.get_by_id(created.id)

        self.assertEqual(fetched.id, created.id)
        self.assertEqual(fetched.username, "getuser")
        self.assertEqual(fetched.email, "get@example.com")
        self.assertEqual(fetched.password_hash, "hash123")
        self.assertEqual(fetched.token_version, 1)

    async def test_get_by_id_not_found(self):
        with self.assertRaises(DoesNotExist):
            await self.repository.get_by_id(99999)

    # ========== get_all ==========

    async def test_get_all_empty(self):
        users = await self.repository.get_all()
        self.assertEqual(len(users), 0)

    async def test_get_all_multiple_users(self):
        await self.repository.create(
            username="user1",
            email="user1@example.com",
            password_hash="hash1",
            token_version=1
        )
        await self.repository.create(
            username="user2",
            email="user2@example.com",
            password_hash="hash2",
            token_version=1
        )
        await self.repository.create(
            username="user3",
            email="user3@example.com",
            password_hash="hash3",
            token_version=2
        )

        users = await self.repository.get_all()

        self.assertEqual(len(users), 3)
        usernames = [u.username for u in users]
        self.assertIn("user1", usernames)
        self.assertIn("user2", usernames)
        self.assertIn("user3", usernames)

    # ========== update_by_id ==========

    async def test_update_by_id_success(self):
        user = await self.repository.create(
            username="olduser",
            email="old@example.com",
            password_hash="oldhash",
            token_version=1
        )

        updated = await self.repository.update_by_id(
            user.id,
            username="newuser",
            email="new@example.com",
            token_version=2
        )

        self.assertEqual(updated.id, user.id)
        self.assertEqual(updated.username, "newuser")
        self.assertEqual(updated.email, "new@example.com")
        self.assertEqual(updated.password_hash, "oldhash")  # unchanged
        self.assertEqual(updated.token_version, 2)

        db_user = await User.get(id=user.id)
        self.assertEqual(db_user.username, "newuser")
        self.assertEqual(db_user.email, "new@example.com")

    async def test_update_by_id_ignore_id_field(self):
        user = await self.repository.create(
            username="original",
            email="original@example.com",
            password_hash="hash",
            token_version=1
        )

        updated = await self.repository.update_by_id(
            user.id,
            id=99999,
            username="updated"
        )

        self.assertEqual(updated.id, user.id)  # id should not change
        self.assertEqual(updated.username, "updated")

    async def test_update_by_id_not_found(self):
        with self.assertRaises(DoesNotExist):
            await self.repository.update_by_id(99999, username="newname")

    # ========== delete_by_id ==========

    async def test_delete_by_id_success(self):
        user = await self.repository.create(
            username="todelete",
            email="delete@example.com",
            password_hash="hash",
            token_version=1
        )

        result = await self.repository.delete_by_id(user.id)

        self.assertTrue(result)

        db_user = await User.get_or_none(id=user.id)
        self.assertIsNone(db_user)

    async def test_delete_by_id_not_found(self):
        with self.assertRaises(DoesNotExist):
            await self.repository.delete_by_id(99999)

    # ========== delete_all ==========

    async def test_delete_all_empty(self):
        result = await self.repository.delete_all()
        self.assertTrue(result)

    async def test_delete_all_with_users(self):
        await self.repository.create(
            username="user1",
            email="user1@example.com",
            password_hash="hash1",
            token_version=1
        )
        await self.repository.create(
            username="user2",
            email="user2@example.com",
            password_hash="hash2",
            token_version=1
        )

        users_before = await User.all()
        self.assertEqual(len(users_before), 2)

        result = await self.repository.delete_all()

        self.assertTrue(result)

        users_after = await User.all()
        self.assertEqual(len(users_after), 0)

    # ========== Edge Cases ==========

    async def test_create_user_with_empty_strings(self):
        user = await self.repository.create(
            username="",
            email="",
            password_hash="",
            token_version=0
        )

        self.assertEqual(user.username, "")
        self.assertEqual(user.email, "")
        self.assertEqual(user.password_hash, "")
        self.assertEqual(user.token_version, 0)

        db_user = await User.get(id=user.id)
        self.assertEqual(db_user.username, "")

    async def test_update_by_id_partial_update(self):
        user = await self.repository.create(
            username="partial",
            email="partial@example.com",
            password_hash="oldhash",
            token_version=1
        )

        updated = await self.repository.update_by_id(
            user.id,
            token_version=5
        )

        self.assertEqual(updated.username, "partial")
        self.assertEqual(updated.email, "partial@example.com")
        self.assertEqual(updated.password_hash, "oldhash")
        self.assertEqual(updated.token_version, 5)

    async def test_multiple_operations_sequence(self):
        # Create
        user = await self.repository.create(
            username="sequence",
            email="seq@example.com",
            password_hash="hash",
            token_version=1
        )

        # Update
        user = await self.repository.update_by_id(user.id, token_version=2)
        self.assertEqual(user.token_version, 2)

        # Get
        fetched = await self.repository.get_by_id(user.id)
        self.assertEqual(fetched.token_version, 2)

        # Delete
        result = await self.repository.delete_by_id(user.id)
        self.assertTrue(result)

        # Verify deleted
        self.assertFalse(await self.repository.id_exists(user.id))