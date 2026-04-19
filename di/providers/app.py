from dishka import Provider, Scope, provide

from logger.setup import LoggingConfigInitializer
from settings import Settings


class AppProvider(Provider):
    scope = Scope.APP

    def __init__(self) -> None:
        super().__init__()

        LoggingConfigInitializer().init()


    @provide
    def settings(self) -> Settings:
        return Settings()