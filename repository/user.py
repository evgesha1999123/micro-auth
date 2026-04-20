from core.repository.repository import BaseDbRepository
from database.tables import User
from model.user import UserSchema


class UserDbRepository(BaseDbRepository[UserSchema, User]):
    async def id_exists(self, id_: int) -> bool:
        user = await self.db_class().get_or_none(id=id_)
        return user is not None

    async def create(self, **kwargs) -> UserSchema:
        if kwargs.get("id"):
            kwargs.pop("id")
        user = await self.db_class().create(**kwargs)
        return self.dto_class(
            id=user.pk,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            token_version=user.token_version
        )

    async def get_by_id(self, id_: int) -> UserSchema:
        user = await self.db_class().get(id=id_)
        return self.dto_class(
            id=user.pk,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            token_version=user.token_version
        )

    async def get_all(self) -> list[UserSchema]:
        users = await self.db_class().all()
        return [
            self.dto_class(
                id=user.pk,
                username=user.username,
                email=user.email,
                password_hash=user.password_hash,
                token_version=user.token_version
            ) for user in users
        ]

    async def update_by_id(self, id_: int, **kwargs) -> UserSchema:
        user = await self.db_class().get(id=id_)
        if kwargs.get("id"):
            kwargs.pop("id")
        await user.update_from_dict(data=kwargs)
        await user.save()
        return self.dto_class(
            id=user.pk,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            token_version=user.token_version
        )

    async def delete_by_id(self, id_: int) -> bool:
        user = await self.db_class().get(id=id_)
        await user.delete()
        user = await self.db_class().get_or_none(id=id_)
        return user is None

    async def delete_all(self) -> bool:
        await self.db_class().all().delete()
        users = await self.db_class().all()
        return len(users) == 0