import logging

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

import di
from api import routers
from api.lifespans import lifespan
from di.providers.app import AppProvider
from settings import Settings

logger = logging.getLogger(__name__)
settings = di.container.get(Settings)
app = FastAPI(
    title='micro-auth',
    lifespan=lifespan,
    version=settings.app.VERSION,
    docs_url="/swagger/docs/",
    redoc_url=None,
)


@app.get("/", include_in_schema=False)
def read_root() -> dict:
    return {"documentation_path": "/swagger/docs/"}


logger.debug(f"Настройки проекта: {settings.app}")

app.include_router(routers.roles_router)
app.include_router(routers.users_router)

setup_dishka(
    container=make_async_container(AppProvider()),
    app=app,
)