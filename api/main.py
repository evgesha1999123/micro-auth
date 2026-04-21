import logging

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from api.exception_handler import ApiExceptionHandler
from core import di
from api import routers
from api.lifespans import lifespan
from core.di import AppProvider
from core.service.exception import RecordAlreadyExistsException, RecordDoesNotExistsException
from service.exceptions import PasswordVerificationFailed, EmailAlreadyExists, UsernameAlreadyExists
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

exception_handler = ApiExceptionHandler(app)

exception_handler.add(RecordAlreadyExistsException, 409, "record_already_exists")
exception_handler.add(RecordDoesNotExistsException, 404, "record_not_found")
exception_handler.add(PasswordVerificationFailed, 401, "Unauthorized")
exception_handler.add(EmailAlreadyExists, 409, "email_already_exists")
exception_handler.add(UsernameAlreadyExists, 409, "username_already_exists")

setup_dishka(
    container=make_async_container(AppProvider()),
    app=app,
)