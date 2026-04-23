from core.service.exception import RecordAlreadyExistsException, RecordDoesNotExistsException
from model.auth import UserRegistrationSchema
from model.user import UserSchema
from repository.user import UserDbRepository
from service.exceptions import PasswordVerificationFailed, UsernameAlreadyExists, EmailAlreadyExists
from utils.password_utils import PasswordUtil


class UserService:
    def __init__(self, user_repo: UserDbRepository, password_util: PasswordUtil) -> None:
        self.repo = user_repo
        self.password_util = password_util


    async def add_user(self, user_registration_schema: UserRegistrationSchema) -> UserSchema | None:
        hashed_pass = self.password_util.get_password_hash(user_registration_schema.password)
        await self.__check_login_exists(user_registration_schema)
        return await self.repo.create(
            username=user_registration_schema.username,
            email=user_registration_schema.email,
            password_hash=hashed_pass,
        )

    async def __check_login_exists(self, user_registration_schema: UserRegistrationSchema) -> None:
        user_conflicts_username = await self.repo.get_by_login(user_registration_schema.username)
        if user_conflicts_username:
            raise UsernameAlreadyExists(user_registration_schema.username)

        user_conflicts_email = await self.repo.get_by_login(user_registration_schema.email)
        if user_conflicts_email:
            raise EmailAlreadyExists(user_registration_schema.email)

    async def change_username(self, old: str, new: str) -> UserSchema:
        old_user = await self.repo.get_by_unique_field(username=old)
        if old_user:
            new_user = await self.repo.get_by_unique_field(username=new)
            if not new_user:
                user = await self.repo.update_by_id(id_=old_user.id, username=new)
                return user if user else None
            raise RecordAlreadyExistsException(new_user)
        raise RecordDoesNotExistsException(username=old)


    async def change_password(self, login: str, old: str, new: str) -> UserSchema:
        user = await self.repo.get_by_login(login=login)
        if user:
            verified = self.password_util.verify_password(
                plain_password=old,
                hashed_password=user.password_hash
            )
            if verified:
                return await self.repo.update_by_id(
                    id_=user.id,
                    password_hash=self.password_util.get_password_hash(new)
                )
            else:
                raise PasswordVerificationFailed(login)
        else:
            raise RecordDoesNotExistsException(login=login)


    async def change_email(self, old: str, new: str) -> UserSchema:
        old_user = await self.repo.get_by_unique_field(email=old)
        if old_user:
            new_user = await self.repo.get_by_unique_field(email=new)
            if not new_user:
                user = await self.repo.update_by_id(id_=old_user.id, email=new)
                return user
            raise RecordAlreadyExistsException(new_user)
        raise RecordDoesNotExistsException(email=old)


    async def get_user(self, login: str) -> UserSchema:
        user = await self.repo.get_by_login(login)
        if user:
            return user
        else:
            raise RecordDoesNotExistsException(login=login)


    async def delete_user(self, user_id: int) -> bool:
        if await self.repo.id_exists(id_=user_id):
            return await self.repo.delete_by_id(id_=user_id)
        raise RecordDoesNotExistsException(user_id=user_id)

    async def get_all(self) -> list[UserSchema]:
        return await self.repo.get_all()