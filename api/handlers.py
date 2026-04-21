from urllib.request import Request

from starlette.responses import JSONResponse

from core.service.exception import RecordAlreadyExistsException, RecordDoesNotExistsException
from service.exceptions import PasswordVerificationFailed


async def record_already_exists_handler(request: Request, exc: RecordAlreadyExistsException) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={
            "error": "record_already_exists",
            "detail": str(exc),
        }
    )


async def record_not_exists_handler(request: Request, exc: RecordDoesNotExistsException) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "error": "record_not_found",
            "detail": str(exc),
        }
    )

async def password_verification_failed_handler(request: Request, exc: PasswordVerificationFailed) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={
            "error": "Unauthorized",
            "detail": str(exc),
        }
    )