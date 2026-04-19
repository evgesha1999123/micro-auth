from contextlib import asynccontextmanager, AsyncExitStack
from typing import AsyncGenerator, Any

from fastapi import FastAPI

from database import db


@asynccontextmanager
async def init_db(_: FastAPI) -> AsyncGenerator[None, Any]:
    await db.init_db()
    yield


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    async with AsyncExitStack() as stack:
        await stack.enter_async_context(init_db(app))
        yield