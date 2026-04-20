from database.db import TORTOISE_ORM
from database.tables import Role
from model.role import RoleSchema
from service.exceptions.base import RecordAlreadyExistsException
from service.user_role.role import RoleService

from unittest import IsolatedAsyncioTestCase
from tortoise import Tortoise


class TestRoleService(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """Инициализация перед каждым тестом"""
        await self.__ensure_connection()
        await Tortoise.generate_schemas()
        self.service = RoleService()
        await self.clear()  # Очищаем БД перед каждым тестом

    async def asyncTearDown(self):
        """Очистка после каждого теста"""
        await self.clear()
        await Tortoise.close_connections()

    @staticmethod
    async def __ensure_connection():
        """Обеспечивает подключение к БД, если оно еще не установлено"""
        if not Tortoise._inited:
            await Tortoise.init(config=TORTOISE_ORM)

    async def clear(self):
        """Очищает таблицу Role"""
        await Role.all().delete()

    async def test_create_role_success(self):
        role = await self.service.create_role("user")

        self.assertIsInstance(role, RoleSchema)
        self.assertEqual(role.role_name, "user")

        db_role = await Role.get(role_name="user")
        self.assertIsNotNone(db_role)
        self.assertEqual(db_role.role_name, "user")

    async def test_create_role_duplicate(self):
        await self.service.create_role("admin")

        with self.assertRaises(RecordAlreadyExistsException):
            await self.service.create_role("admin")

    async def test_get_by_id(self):
        role = await self.service.create_role("manager")

        fetched = await self.service.get_by_id(role.id)

        self.assertEqual(fetched.id, role.id)
        self.assertEqual(fetched.role_name, "manager")

    async def test_get_by_name(self):
        await self.service.create_role("moderator")

        fetched = await self.service.get_by_name("moderator")

        self.assertEqual(fetched.role_name, "moderator")

    async def test_change_role_name_by_id(self):
        # Создаем роль
        role = await self.service.create_role("old_name")

        # Обновляем имя роли
        updated = await self.service.change_role_name_by_id(role.id, "new_name")

        # Проверяем возвращаемый объект
        self.assertEqual(updated.role_name, "new_name")

        # Проверяем в базе данных
        db_role = await Role.get(id=role.id)
        self.assertEqual(db_role.role_name, "new_name")

        # Дополнительная проверка: старая роль должна отсутствовать
        old_role = await Role.get_or_none(role_name="old_name")
        self.assertIsNone(old_role)

    async def test_change_role_name_by_name(self):
        await self.service.create_role("old")

        updated = await self.service.change_role_name_by_name("old", "new")

        self.assertEqual(updated.role_name, "new")

        # Проверяем в базе данных
        db_role = await Role.get(role_name="new")
        self.assertIsNotNone(db_role)

        # Старое имя не должно существовать
        old_role = await Role.get_or_none(role_name="old")
        self.assertIsNone(old_role)

    async def test_delete_role(self):
        role = await self.service.create_role("to_delete")

        result = await self.service.delete_role(role.id)

        self.assertTrue(result)

        db_role = await Role.get_or_none(id=role.id)
        self.assertIsNone(db_role)

    async def test_get_all(self):
        await self.service.create_role("r1")
        await self.service.create_role("r2")

        roles = await self.service.get_all()

        self.assertEqual(len(roles), 2)
        self.assertTrue(all(isinstance(r, RoleSchema) for r in roles))

        # Проверяем имена ролей
        role_names = [r.role_name for r in roles]
        self.assertIn("r1", role_names)
        self.assertIn("r2", role_names)