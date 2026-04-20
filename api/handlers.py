from urllib.request import Request

from starlette.responses import JSONResponse

from core.service.exception import RecordAlreadyExistsException, RecordDoesNotExistsException


async def record_already_exists_handler(request: Request, exc: RecordAlreadyExistsException):
    return JSONResponse(
        status_code=409,  # Conflict
        content={
            "error": "record_already_exists",
            "detail": str(exc),
        }
    )


async def record_not_exists_handler(request: Request, exc: RecordDoesNotExistsException):
    return JSONResponse(
        status_code=404,  # Not Found
        content={
            "error": "record_not_found",
            "detail": str(exc),
        }
    )