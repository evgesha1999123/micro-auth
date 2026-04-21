from dishka import Provider, Scope, provide

from database.tables import Role, User
from logger.setup import LoggingConfigInitializer
from model.role import RoleSchema
from model.user import UserSchema
from repository.role import RoleDbRepository
from repository.user import UserDbRepository
from service.role import RoleService
from service.user import UserService
from settings import Settings
from utils.password_utils import PasswordUtil


class AppProvider(Provider):
    scope = Scope.APP

    def __init__(self) -> None:
        super().__init__()
        self.settings = Settings()
        LoggingConfigInitializer().init()


    @provide
    def settings(self) -> Settings:
        return Settings()

    @provide
    def role_service(self) -> RoleService:
        return RoleService(RoleDbRepository(dto_class=RoleSchema, db_class=Role))

    @provide
    def user_repo(self) -> UserDbRepository:
        return UserDbRepository(dto_class=UserSchema, db_class=User)

    @provide
    def password_util(self) -> PasswordUtil:
        return PasswordUtil(algorythm=self.settings.app.HASH_ALGORYTHM)

    @provide
    def user_service(self) -> UserService:
        return UserService(
            user_repo=UserDbRepository(dto_class=UserSchema, db_class=User),
            password_util=self.password_util()
        )