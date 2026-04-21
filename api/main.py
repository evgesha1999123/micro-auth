import logging

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from api.handlers import record_already_exists_handler, record_not_exists_handler, password_verification_failed_handler
from core import di
from api import routers
from api.lifespans import lifespan
from core.di import AppProvider
from core.service.exception import RecordAlreadyExistsException, RecordDoesNotExistsException
from service.exceptions import PasswordVerificationFailed
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
app.include_router(routers.auth_router)
app.include_router(routers.user_role_router)

app.add_exception_handler(RecordAlreadyExistsException, record_already_exists_handler)
app.add_exception_handler(RecordDoesNotExistsException, record_not_exists_handler)
app.add_exception_handler(PasswordVerificationFailed, password_verification_failed_handler)

setup_dishka(
    container=make_async_container(AppProvider()),
    app=app,
)