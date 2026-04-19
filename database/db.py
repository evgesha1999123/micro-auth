import asyncio
import logging
from contextlib import asynccontextmanager
from functools import wraps
from typing import AsyncGenerator, Awaitable, Callable, TypeVar

from tortoise import BaseDBAsyncClient, Tortoise, connections

import di
from settings import Settings

logger = logging.getLogger(__name__)
settings = di.container.get(Settings)

T = TypeVar("T")
P = TypeVar("P")


TORTOISE_ORM = {
    "connections": {
        "default": settings.db.get_connection_config(),
    },
    "apps": {
        "models": {
            "models": ["aerich.models", "database.tables"],
            "default_connection": "default",
        },
    },
    "use_tz": False,
}


def log_connection(db_config: dict) -> None:
    conn_alias = db_config["apps"]["models"]['default_connection']
    credentials: dict = db_config["connections"][conn_alias]['credentials']
    database = credentials["database"]
    host = credentials["host"]
    port = credentials["port"]
    logger.info(f"БД подключена: {database=}, {host=}, {port=}")


async def init_db() -> None:
    await Tortoise.init(config=TORTOISE_ORM)
    log_connection(TORTOISE_ORM)


def tortoise_connect(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
    @wraps(func)
    async def wrapper(*args: P, **kwargs: T) -> T:
        try:
            await Tortoise.init(config=TORTOISE_ORM)
            return await func(*args, **kwargs)
        finally:
            await Tortoise.close_connections()

    return wrapper


@asynccontextmanager
async def get_conn(conn_alias: str) -> AsyncGenerator[BaseDBAsyncClient, None]:
    conn: BaseDBAsyncClient = connections.get(conn_alias=conn_alias)
    try:
        logger.debug(f"Выдача соединения: {conn_alias}")
        yield conn
    finally:
        logger.debug(f"Закрытие соединения: {conn_alias}")
        await conn.close()


@tortoise_connect
async def raw_execute(conn_alias: str, sql: str) -> list[dict]:
    async with get_conn(conn_alias=conn_alias) as conn:
        data = await conn.execute_query_dict(sql)
    return data


async def show_models() -> None:
    await Tortoise.init(config=TORTOISE_ORM)
    models = Tortoise.apps.get("models")  # Получаем все модели
    print("Зарегистрированные модели:")
    print(models)


async def generate_schemas() -> None:
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


if __name__ == '__main__':
    asyncio.run(generate_schemas())
