from tortoise import fields

from database.tables.base_mixin import BaseMixin


class Role(BaseMixin):
    role_name = fields.CharField(max_length=255, unique=True)

    class Meta:
        table = "role"
        table_description = "Таблица ролей для пользователей"

    def __str__(self) -> str:
        return f"<Role: {self.pk} - {self.role_name}>"