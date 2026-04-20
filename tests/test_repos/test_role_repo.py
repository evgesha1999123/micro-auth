import unittest
from unittest import IsolatedAsyncioTestCase

from tortoise import Tortoise
from tortoise.exceptions import DoesNotExist

from database.db import TORTOISE_ORM
from database.tables import Role
from model.role import RoleSchema
from core.service.exception import RecordAlreadyExistsException
from repository.role import RoleDbRepository


class TestRoleDbRepository(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        await self.__ensure_connection()
        await Tortoise.generate_schemas()
        self.repository = RoleDbRepository(
            dto_class=RoleSchema,
            db_class=Role
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
        await Role.all().delete()

    # ========== id_exists ==========

    async def test_id_exists_true(self):
        role = await self.repository.create("user")
        self.assertTrue(await self.repository.id_exists(role[0].id))

    async def test_id_exists_false(self):
        self.assertFalse(await self.repository.id_exists(99999))

    # ========== role_name_exists ==========

    async def test_role_name_exists_true(self):
        await self.repository.create("admin")
        self.assertTrue(await self.repository.role_name_exists("admin"))

    async def test_role_name_exists_false(self):
        self.assertFalse(await self.repository.role_name_exists("nope"))

    # ========== create ==========

    async def test_create_role_success(self):
        role, created = await self.repository.create("user")

        self.assertTrue(created)
        self.assertEqual(role.role_name, "user")

        db_role = await Role.get(role_name="user")
        self.assertIsNotNone(db_role)

    async def test_create_role_duplicate(self):
        await self.repository.create("admin")

    # ========== get_by_id ==========

    async def test_get_by_id_success(self):
        created, _ = await self.repository.create("manager")

        fetched = await self.repository.get_by_id(created.id)

        self.assertEqual(fetched.role_name, "manager")

    async def test_get_by_id_not_found(self):
        with self.assertRaises(DoesNotExist):
            await self.repository.get_by_id(99999)

    # ========== get_by_name ==========

    async def test_get_by_name_success(self):
        await self.repository.create("moderator")

        fetched = await self.repository.get_by_name("moderator")

        self.assertEqual(fetched.role_name, "moderator")

    async def test_get_by_name_not_found(self):
        with self.assertRaises(DoesNotExist):
            await self.repository.get_by_name("none")

    # ========== get_all ==========

    async def test_get_all(self):
        await self.repository.create("r1")
        await self.repository.create("r2")

        roles = await self.repository.get_all()

        self.assertEqual(len(roles), 2)

    # ========== update_by_id ==========

    async def test_update_by_id_success(self):
        role, _ = await self.repository.create("old")

        updated = await self.repository.update_by_id(role.id, "new")

        self.assertEqual(updated.role_name, "new")

    async def test_update_by_id_not_found(self):
        with self.assertRaises(DoesNotExist):
            await self.repository.update_by_id(99999, "x")

    # ========== update_by_name ==========

    async def test_update_by_name_success(self):
        await self.repository.create("old")

        updated = await self.repository.update_by_name("old", "new")

        self.assertEqual(updated.role_name, "new")

    async def test_update_by_name_not_found(self):
        with self.assertRaises(DoesNotExist):
            await self.repository.update_by_name("x", "y")

    # ========== delete_by_id ==========

    async def test_delete_by_id_success(self):
        role, _ = await self.repository.create("to_delete")

        result = await self.repository.delete_by_id(role.id)

        self.assertTrue(result)

    async def test_delete_by_id_not_found(self):
        with self.assertRaises(DoesNotExist):
            await self.repository.delete_by_id(99999)

    # ========== delete_by_name ==========

    async def test_delete_by_name_success(self):
        await self.repository.create("to_delete")

        result = await self.repository.delete_by_name("to_delete")

        self.assertTrue(result)

    async def test_delete_by_name_not_found(self):
        with self.assertRaises(DoesNotExist):
            await self.repository.delete_by_name("none")

    # ========== delete_all ==========

    async def test_delete_all(self):
        await self.repository.create("r1")
        await self.repository.create("r2")

        result = await self.repository.delete_all()

        self.assertTrue(result)