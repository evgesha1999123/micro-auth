from dishka import Provider, Scope, provide

from database.tables import Role
from logger.setup import LoggingConfigInitializer
from model.role import RoleSchema
from repository.role import RoleDbRepository
from service.role import RoleService
from settings import Settings


class AppProvider(Provider):
    scope = Scope.APP

    def __init__(self) -> None:
        super().__init__()
        LoggingConfigInitializer().init()


    @provide
    def settings(self) -> Settings:
        return Settings()

    @provide
    def role_service(self) -> RoleService:
        return RoleService(RoleDbRepository(dto_class=RoleSchema, db_class=Role))