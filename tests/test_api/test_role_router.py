from unittest import TestCase
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from model.role import RoleSchema
from core.service.exception import (
    RecordAlreadyExistsException,
    RecordDoesNotExistsException
)


class TestRoleRouter(TestCase):

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.app = FastAPI()

        # Создаем мок для сервиса
        self.mock_service = AsyncMock()

        # Патчим сервис
        self.service_patcher = patch('api.routers.roles.service', self.mock_service)
        self.mock_service = self.service_patcher.start()

        # Импортируем роутер ПОСЛЕ патча
        from api.routers.roles import router
        self.app.include_router(router)
        self.client = TestClient(self.app)

        self.sample_role = RoleSchema(id=1, role_name="admin")
        self.sample_role2 = RoleSchema(id=2, role_name="user")

        # Настройка моков по умолчанию
        self._setup_default_mocks()

    def _setup_default_mocks(self):
        """Настройка моков по умолчанию"""
        self.mock_service.create_role = AsyncMock()
        self.mock_service.get_by_id = AsyncMock()
        self.mock_service.get_by_name = AsyncMock()
        self.mock_service.change_name_by_id = AsyncMock()
        self.mock_service.change_name_by_old_name = AsyncMock()
        self.mock_service.delete_by_id = AsyncMock()
        self.mock_service.delete_by_name = AsyncMock()
        self.mock_service.get_all = AsyncMock()
        self.mock_service.delete_all = AsyncMock()

    def tearDown(self):
        """Очистка после каждого теста"""
        self.service_patcher.stop()

    # ========== CREATE ROLE ==========

    def test_create_role_success(self):
        """Тест успешного создания роли"""
        self.mock_service.create_role.return_value = self.sample_role

        response = self.client.post("/roles/", params={"name": "admin"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "id": 1,
            "role_name": "admin"
        })
        self.mock_service.create_role.assert_called_once_with("admin")

    def test_create_role_already_exists(self):
        """Тест создания уже существующей роли"""
        self.mock_service.create_role.side_effect = RecordAlreadyExistsException(self.sample_role)

        response = self.client.post("/roles/", params={"name": "admin"})

        self.assertEqual(response.status_code, 409)

    # ========== GET BY ID ==========

    def test_get_role_by_id_success(self):
        """Тест успешного получения роли по ID"""
        self.mock_service.get_by_id.return_value = self.sample_role

        response = self.client.get("/roles/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "id": 1,
            "role_name": "admin"
        })
        self.mock_service.get_by_id.assert_called_once_with(1)

    def test_get_role_by_id_not_found(self):
        """Тест получения несуществующей роли по ID"""
        self.mock_service.get_by_id.side_effect = RecordDoesNotExistsException(id=999)

        response = self.client.get("/roles/999")

        self.assertEqual(response.status_code, 404)

    def test_get_role_by_id_invalid_type(self):
        """Тест получения роли с невалидным ID"""
        response = self.client.get("/roles/invalid")

        self.assertEqual(response.status_code, 422)

    # ========== GET BY NAME ==========

    def test_get_role_by_name_success(self):
        """Тест успешного получения роли по имени"""
        self.mock_service.get_by_name.return_value = self.sample_role

        response = self.client.get("/roles/name/admin")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "id": 1,
            "role_name": "admin"
        })
        self.mock_service.get_by_name.assert_called_once_with("admin")

    def test_get_role_by_name_not_found(self):
        """Тест получения несуществующей роли по имени"""
        self.mock_service.get_by_name.side_effect = RecordDoesNotExistsException(role_name="nonexistent")

        response = self.client.get("/roles/name/nonexistent")

        self.assertEqual(response.status_code, 404)

    # ========== CHANGE NAME BY ID ==========

    def test_change_name_by_id_success(self):
        """Тест успешного изменения имени роли по ID"""
        updated_role = RoleSchema(id=1, role_name="new_admin")
        self.mock_service.change_name_by_id.return_value = updated_role

        response = self.client.put(
            "/roles/1",
            params={"new_name": "new_admin"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "id": 1,
            "role_name": "new_admin"
        })
        self.mock_service.change_name_by_id.assert_called_once_with(1, "new_admin")

    def test_change_name_by_id_not_found(self):
        """Тест изменения имени несуществующей роли"""
        self.mock_service.change_name_by_id.side_effect = RecordDoesNotExistsException(id=999)

        response = self.client.put("/roles/999", params={"new_name": "new"})

        # УБИРАЕМ ЭТУ СТРОКУ - она неправильная:
        # self.assertRaises(RecordDoesNotExistsException)

        self.assertEqual(response.status_code, 404)

    def test_change_name_by_id_conflict(self):
        """Тест изменения имени на уже существующее"""
        existing_role = RoleSchema(id=2, role_name="existing")
        self.mock_service.change_name_by_id.side_effect = RecordAlreadyExistsException(existing_role)

        response = self.client.put("/roles/1", params={"new_name": "existing"})

        self.assertEqual(response.status_code, 409)

    # ========== CHANGE NAME BY OLD NAME ==========

    def test_change_name_by_old_name_success(self):
        """Тест успешного изменения имени роли по старому имени"""
        updated_role = RoleSchema(id=1, role_name="new_admin")
        self.mock_service.change_name_by_old_name.return_value = updated_role

        response = self.client.put(
            "/roles/name/old_admin",
            params={"new_name": "new_admin"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "id": 1,
            "role_name": "new_admin"
        })
        self.mock_service.change_name_by_old_name.assert_called_once_with("old_admin", "new_admin")

    def test_change_name_by_old_name_not_found(self):
        """Тест изменения имени несуществующей роли"""
        self.mock_service.change_name_by_old_name.side_effect = RecordDoesNotExistsException(role_name="old")

        response = self.client.put("/roles/name/old", params={"new_name": "new"})

        self.assertEqual(response.status_code, 404)

    def test_change_name_by_old_name_conflict(self):
        """Тест изменения имени на уже существующее"""
        existing_role = RoleSchema(id=2, role_name="new")
        self.mock_service.change_name_by_old_name.side_effect = RecordAlreadyExistsException(existing_role)

        response = self.client.put("/roles/name/old", params={"new_name": "new"})

        self.assertEqual(response.status_code, 409)

    # ========== DELETE BY ID ==========

    def test_delete_by_id_success(self):
        """Тест успешного удаления роли по ID"""
        self.mock_service.delete_by_id.return_value = True

        response = self.client.delete("/roles/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), True)
        self.mock_service.delete_by_id.assert_called_once_with(1)

    def test_delete_by_id_not_found(self):
        """Тест удаления несуществующей роли по ID"""
        self.mock_service.delete_by_id.side_effect = RecordDoesNotExistsException(id=999)

        response = self.client.delete("/roles/999")

        self.assertEqual(response.status_code, 404)

    # ========== DELETE BY NAME ==========

    def test_delete_by_name_success(self):
        """Тест успешного удаления роли по имени"""
        self.mock_service.delete_by_name.return_value = True

        response = self.client.delete("/roles/name/admin")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), True)
        self.mock_service.delete_by_name.assert_called_once_with("admin")

    def test_delete_by_name_not_found(self):
        """Тест удаления несуществующей роли по имени"""
        self.mock_service.delete_by_name.side_effect = RecordDoesNotExistsException(role_name="nonexistent")

        response = self.client.delete("/roles/name/nonexistent")

        self.assertEqual(response.status_code, 404)

    # ========== GET ALL ==========

    def test_get_all_roles_success(self):
        """Тест успешного получения всех ролей"""
        all_roles = [self.sample_role, self.sample_role2]
        self.mock_service.get_all.return_value = all_roles

        response = self.client.get("/roles/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["role_name"], "admin")
        self.assertEqual(response.json()[1]["role_name"], "user")
        self.mock_service.get_all.assert_called_once()

    def test_get_all_roles_empty(self):
        """Тест получения списка ролей когда он пуст"""
        self.mock_service.get_all.return_value = []

        response = self.client.get("/roles/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    # ========== DELETE ALL ==========

    def test_delete_all_roles_success(self):
        """Тест успешного удаления всех ролей"""
        self.mock_service.delete_all.return_value = True

        response = self.client.delete("/roles/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), True)
        self.mock_service.delete_all.assert_called_once()

    def test_delete_all_roles_failure(self):
        """Тест неудачного удаления всех ролей"""
        self.mock_service.delete_all.return_value = False

        response = self.client.delete("/roles/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), False)