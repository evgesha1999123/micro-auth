from tortoise import Model, fields


class ActualMixin:
    active = fields.BooleanField(default=True)
    deleted = fields.BooleanField(default=False)


class TimestampMixin:
    created_at = fields.DatetimeField(
        auto_now_add=True, description="Дата и время создания записи", null=False
    )
    updated_at = fields.DatetimeField(
        auto_now=True,
        description="Дата и время последнего обновления записи",
        null=False,
    )

class BaseMixin(Model, ActualMixin, TimestampMixin):
    pass