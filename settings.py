# mypy: ignore-errors
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from utils.password_utils import PassHashAlgorythm


class FromEnvFile(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(Path(__file__).resolve().parent, ".env"),
        extra="ignore",
    )


class BaseConnection(FromEnvFile):
    USER: str
    PASS: str
    HOST: str
    PORT: int
    NAME: str

    def get_connection_config(self) -> dict:
        return {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": self.HOST,
                "port": self.PORT,
                "user": self.USER,
                "password": self.PASS,
                "database": self.NAME,
            },
        }


class DefaultDB(BaseConnection):
    model_config = SettingsConfigDict(env_prefix="DEFAULT_DB_")


class TestDB(BaseConnection):
    model_config = SettingsConfigDict(env_prefix="TEST_DB_")


class App(FromEnvFile):
    model_config = SettingsConfigDict(env_prefix="APP_")
    SERVER_PORT: int
    VERSION: str = '0.0.1'  # bump2version autogenerate. DO NOT EDIT
    USE_TEST_DB: bool
    PASS_HASH_ALGORYTHM: PassHashAlgorythm


class API(FromEnvFile):
    model_config = SettingsConfigDict(env_prefix="API_")
    KEY: str


class Swagger(FromEnvFile):
    model_config = SettingsConfigDict(env_prefix="SWAGGER_")
    LOGIN: str
    PASSWORD: str


class JWT(FromEnvFile):
    model_config = SettingsConfigDict(env_prefix="JWT_")
    SECRET_KEY: str
    EXPIRES_SECONDS: int
    ALGORYTHM: str


# --- Implementation ---
class Settings(BaseSettings):
    app: App = Field(default_factory=App)
    db: DefaultDB = Field(default_factory=DefaultDB)
    test_db: TestDB = Field(default_factory=TestDB)
    jwt: JWT = Field(default_factory=JWT)
    api: API = Field(default_factory=API)
    swagger: Swagger = Field(default_factory=Swagger)


if __name__ == '__main__':
    settings = Settings()
    print(settings.app)