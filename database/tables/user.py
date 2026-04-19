from tortoise import fields

from database.tables.base_mixin import BaseMixin


class User(BaseMixin):
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, unique=True, null=True)
    password_hash = fields.CharField(max_length=255)
    token_version = fields.IntField(default=0)

    roles = fields.ManyToManyField("models.Role", related_name='users', on_delete=fields.CASCADE)

    class Meta:
        table = "user"
        table_description = "Таблица пользователей"

    def __str__(self) -> str:
        return f"<User: {self.pk} - {self.username} - {self.email}>"