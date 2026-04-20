import unittest
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock

from tortoise import Tortoise

from database.db import TORTOISE_ORM
from database.tables import Role
from model.role import RoleSchema
from service.exceptions.base import RecordAlreadyExistsException
from service.user_role.role import RoleDbService


class TestRoleDbService(IsolatedAsyncioTestCase):
    """Тесты для RoleDbService с реальной БД"""

    async def asyncSetUp(self):
        """Инициализация перед каждым тестом"""
        await self.__ensure_connection()
        await Tortoise.generate_schemas()
        self.service = RoleDbService(
            dto_class=RoleSchema,
            db_class=Role
        )
        await self.clear()

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

    # ========== Тесты для create ==========
    async def test_create_role_success(self):
        """Успешное создание роли"""
        params = RoleSchema(role_name="user")
        role = await self.service.create(params)

        self.assertIsInstance(role, RoleSchema)
        self.assertEqual(role.role_name, "user")
        self.assertIsNotNone(role.id)

        db_role = await Role.get(role_name="user")
        self.assertIsNotNone(db_role)
        self.assertEqual(db_role.role_name, "user")

    async def test_create_role_with_id_ignored(self):
        """Создание роли с id в params - id должен игнорироваться"""
        params = RoleSchema(id=999, role_name="test_role")
        role = await self.service.create(params)

        self.assertNotEqual(role.id, 999)  # id не должен быть 999
        self.assertEqual(role.role_name, "test_role")

    async def test_create_role_duplicate(self):
        """Создание дубликата роли - должно быть исключение"""
        params = RoleSchema(role_name="admin")
        await self.service.create(params)

        with self.assertRaises(RecordAlreadyExistsException):
            await self.service.create(params)

    async def test_create_role_empty_name(self):
        """Создание роли с пустым именем"""
        params = RoleSchema(role_name="")
        role = await self.service.create(params)

        self.assertEqual(role.role_name, "")
        db_role = await Role.get(role_name="")
        self.assertIsNotNone(db_role)

    # ========== Тесты для get_by_id ==========
    async def test_get_by_id_success(self):
        """Успешное получение роли по ID"""
        created = await self.service.create(RoleSchema(role_name="manager"))

        params = RoleSchema(id=created.id)
        fetched = await self.service.get_by_id(params)

        self.assertEqual(fetched.id, created.id)
        self.assertEqual(fetched.role_name, "manager")

    async def test_get_by_id_not_found(self):
        """Получение несуществующей роли по ID"""
        params = RoleSchema(id=99999)

        with self.assertRaises(Exception):  # Role.get выбрасывает DoesNotExist
            await self.service.get_by_id(params)

    # ========== Тесты для get_by_name ==========
    async def test_get_by_name_success(self):
        """Успешное получение роли по имени"""
        await self.service.create(RoleSchema(role_name="moderator"))

        params = RoleSchema(role_name="moderator")
        fetched = await self.service.get_by_name(params)

        self.assertEqual(fetched.role_name, "moderator")
        self.assertIsNotNone(fetched.id)

    async def test_get_by_name_not_found(self):
        """Получение несуществующей роли по имени"""
        params = RoleSchema(role_name="nonexistent")

        with self.assertRaises(Exception):
            await self.service.get_by_name(params)

    async def test_get_by_name_case_sensitive(self):
        """Поиск по имени чувствителен к регистру"""
        await self.service.create(RoleSchema(role_name="Admin"))

        params_lower = RoleSchema(role_name="admin")
        params_upper = RoleSchema(role_name="Admin")

        with self.assertRaises(Exception):
            await self.service.get_by_name(params_lower)

        fetched = await self.service.get_by_name(params_upper)
        self.assertEqual(fetched.role_name, "Admin")

    # ========== Тесты для get_all ==========
    async def test_get_all_empty(self):
        """Получение всех ролей из пустой БД"""
        roles = await self.service.get_all()

        self.assertEqual(len(roles), 0)
        self.assertIsInstance(roles, list)

    async def test_get_all_without_filters(self):
        """Получение всех ролей без фильтров"""
        await self.service.create(RoleSchema(role_name="r1"))
        await self.service.create(RoleSchema(role_name="r2"))
        await self.service.create(RoleSchema(role_name="r3"))

        roles = await self.service.get_all()

        self.assertEqual(len(roles), 3)
        self.assertTrue(all(isinstance(r, RoleSchema) for r in roles))
        role_names = [r.role_name for r in roles]
        self.assertIn("r1", role_names)
        self.assertIn("r2", role_names)
        self.assertIn("r3", role_names)

    async def test_get_all_with_filters(self):
        """Получение всех ролей с фильтрацией"""
        await self.service.create(RoleSchema(role_name="active_user"))
        await self.service.create(RoleSchema(role_name="inactive_user"))
        await self.service.create(RoleSchema(role_name="admin_user"))

        # Фильтр по части имени
        roles = await self.service.get_all()

        self.assertEqual(len(roles), 3)
        role_names = [r.role_name for r in roles]
        self.assertIn("active_user", role_names)
        self.assertIn("inactive_user", role_names)
        self.assertIn("admin_user", role_names)

    async def test_get_all_with_empty_filters(self):
        await self.service.create(RoleSchema(role_name="test"))

        roles = await self.service.get_all()

        self.assertEqual(len(roles), 1)

    # ========== Тесты для update_by_id ==========
    async def test_update_by_id_success(self):
        """Успешное обновление роли по ID"""
        old_role = await self.service.create(RoleSchema(role_name="old_name"))

        old_params = RoleSchema(id=old_role.id)
        new_params = RoleSchema(role_name="new_name")

        updated = await self.service.update_by_id(old_params, new_params)

        self.assertEqual(updated.role_name, "new_name")
        self.assertEqual(updated.id, old_role.id)

        # Проверяем в БД
        db_role = await Role.get(id=old_role.id)
        self.assertEqual(db_role.role_name, "new_name")

        # Старая роль не должна существовать
        old_db_role = await Role.get_or_none(role_name="old_name")
        self.assertIsNone(old_db_role)

    async def test_update_by_id_not_found(self):
        """Обновление несуществующей роли по ID"""
        old_params = RoleSchema(id=99999)
        new_params = RoleSchema(role_name="new_name")

        with self.assertRaises(Exception):
            await self.service.update_by_id(old_params, new_params)

    async def test_update_by_id_same_name(self):
        """Обновление роли на то же имя"""
        role = await self.service.create(RoleSchema(role_name="same_name"))

        old_params = RoleSchema(id=role.id)
        new_params = RoleSchema(role_name="same_name")

        updated = await self.service.update_by_id(old_params, new_params)

        self.assertEqual(updated.role_name, "same_name")

        # Проверяем, что дубликат не создался
        count = await Role.all().count()
        self.assertEqual(count, 1)

    # ========== Тесты для update_by_name ==========
    async def test_update_by_name_success(self):
        """Успешное обновление роли по имени"""
        await self.service.create(RoleSchema(role_name="old"))

        old_params = RoleSchema(role_name="old")
        new_params = RoleSchema(role_name="new")

        updated = await self.service.update_by_name(old_params, new_params)

        self.assertEqual(updated.role_name, "new")

        # Проверяем в БД
        db_role = await Role.get(role_name="new")
        self.assertIsNotNone(db_role)

        old_db_role = await Role.get_or_none(role_name="old")
        self.assertIsNone(old_db_role)

    async def test_update_by_name_not_found(self):
        """Обновление несуществующей роли по имени"""
        old_params = RoleSchema(role_name="nonexistent")
        new_params = RoleSchema(role_name="new_name")

        with self.assertRaises(Exception):
            await self.service.update_by_name(old_params, new_params)

    # ========== Тесты для delete_by_id ==========
    async def test_delete_by_id_success(self):
        """Успешное удаление роли по ID"""
        role = await self.service.create(RoleSchema(role_name="to_delete"))

        params = RoleSchema(id=role.id)
        result = await self.service.delete_by_id(params)

        self.assertTrue(result)

        db_role = await Role.get_or_none(id=role.id)
        self.assertIsNone(db_role)

    async def test_delete_by_id_not_found(self):
        """Удаление несуществующей роли по ID"""
        params = RoleSchema(id=99999)

        with self.assertRaises(Exception):
            await self.service.delete_by_id(params)

    async def test_delete_by_id_twice(self):
        """Повторное удаление одной и той же роли"""
        role = await self.service.create(RoleSchema(role_name="delete_twice"))

        params = RoleSchema(id=role.id)
        first_delete = await self.service.delete_by_id(params)
        self.assertTrue(first_delete)

        with self.assertRaises(Exception):
            await self.service.delete_by_id(params)

    # ========== Тесты для delete_by_name ==========
    async def test_delete_by_name_success(self):
        """Успешное удаление роли по имени"""
        await self.service.create(RoleSchema(role_name="to_delete_by_name"))

        params = RoleSchema(role_name="to_delete_by_name")
        result = await self.service.delete_by_name(params)

        self.assertTrue(result)

        db_role = await Role.get_or_none(role_name="to_delete_by_name")
        self.assertIsNone(db_role)

    async def test_delete_by_name_not_found(self):
        """Удаление несуществующей роли по имени"""
        params = RoleSchema(role_name="nonexistent")

        with self.assertRaises(Exception):
            await self.service.delete_by_name(params)

    async def test_delete_by_name_case_sensitive(self):
        """Удаление роли с учетом регистра имени"""
        await self.service.create(RoleSchema(role_name="DeleteMe"))

        params_wrong_case = RoleSchema(role_name="deleteme")
        params_correct = RoleSchema(role_name="DeleteMe")

        with self.assertRaises(Exception):
            await self.service.delete_by_name(params_wrong_case)

        result = await self.service.delete_by_name(params_correct)
        self.assertTrue(result)

    # ========== Тесты для delete_all ==========
    async def test_delete_all_empty(self):
        """Удаление всех ролей из пустой БД"""
        result = await self.service.delete_all()

        self.assertTrue(result)  # Пустая БД считается пустой
        roles = await Role.all()
        self.assertEqual(len(roles), 0)

    async def test_delete_all_with_data(self):
        """Удаление всех ролей с данными"""
        await self.service.create(RoleSchema(role_name="r1"))
        await self.service.create(RoleSchema(role_name="r2"))
        await self.service.create(RoleSchema(role_name="r3"))

        # Проверяем, что данные есть
        roles_before = await Role.all()
        self.assertEqual(len(roles_before), 3)

        result = await self.service.delete_all()

        self.assertTrue(result)
        roles_after = await Role.all()
        self.assertEqual(len(roles_after), 0)

    async def test_delete_all_with_filters_param(self):
        """Метод delete_all игнорирует параметр params"""
        await self.service.create(RoleSchema(role_name="keep1"))
        await self.service.create(RoleSchema(role_name="keep2"))

        # Передаем params, но delete_all удаляет всё
        params = RoleSchema(role_name="keep1")
        result = await self.service.delete_all()

        self.assertTrue(result)
        roles = await Role.all()
        self.assertEqual(len(roles), 0)  # Удалились все, не только с именем keep1

    # ========== Интеграционные тесты ==========
    async def test_full_crud_cycle(self):
        """Полный цикл CRUD операций"""
        # Create
        created = await self.service.create(RoleSchema(role_name="crud_test"))
        self.assertIsNotNone(created.id)

        # Read by ID
        fetched_by_id = await self.service.get_by_id(RoleSchema(id=created.id))
        self.assertEqual(fetched_by_id.role_name, "crud_test")

        # Read by name
        fetched_by_name = await self.service.get_by_name(RoleSchema(role_name="crud_test"))
        self.assertEqual(fetched_by_name.id, created.id)

        # Update
        updated = await self.service.update_by_id(
            RoleSchema(id=created.id),
            RoleSchema(role_name="crud_test_updated")
        )
        self.assertEqual(updated.role_name, "crud_test_updated")

        # Read all
        all_roles = await self.service.get_all()
        self.assertEqual(len(all_roles), 1)

        # Delete
        deleted = await self.service.delete_by_id(RoleSchema(id=created.id))
        self.assertTrue(deleted)

        # Verify deleted
        all_roles_after = await self.service.get_all()
        self.assertEqual(len(all_roles_after), 0)

    async def test_concurrent_operations(self):
        """Параллельные операции с ролями"""
        import asyncio

        # Создаем несколько ролей параллельно
        tasks = [
            self.service.create(RoleSchema(role_name=f"concurrent_{i}"))
            for i in range(5)
        ]
        roles = await asyncio.gather(*tasks)

        self.assertEqual(len(roles), 5)

        # Параллельное чтение
        read_tasks = [
            self.service.get_by_id(RoleSchema(id=role.id))
            for role in roles
        ]
        fetched_roles = await asyncio.gather(*read_tasks)

        self.assertEqual(len(fetched_roles), 5)


class TestRoleDbServiceMock(unittest.IsolatedAsyncioTestCase):
    """Тесты с моками для изоляции"""

    def setUp(self):
        """Настройка моков"""
        self.mock_db_class = MagicMock()
        self.mock_dto_class = MagicMock()

        self.service = RoleDbService(
            dto_class=self.mock_dto_class,
            db_class=self.mock_db_class
        )

    async def test_create_handles_dict_conversion(self):
        """Тест преобразования DTO в словарь"""
        mock_role = MagicMock()
        mock_role.pk = 1
        mock_role.role_name = "test"

        self.mock_db_class.get_or_create = AsyncMock(return_value=(mock_role, True))
        self.mock_dto_class.return_value = MagicMock(id=1, role_name="test")

        params = MagicMock()
        params.model_dump.return_value = {"id": 1, "role_name": "test"}

        result = await self.service.create(params)

        # Проверяем, что id был удален из словаря
        call_args = self.mock_db_class.get_or_create.call_args[1]
        self.assertNotIn("id", call_args)
        self.assertEqual(call_args["role_name"], "test")


if __name__ == '__main__':
    unittest.main()
