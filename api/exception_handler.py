from typing import Optional, Type

from fastapi import Request, FastAPI
from starlette.responses import JSONResponse


class ApiExceptionHandler:
    def __init__(self, app: FastAPI) -> None:
        self.app = app

    def add(
            self,
            err: Type[Exception],
            status_code: int,
            err_msg: str,
            err_detail: Optional[str] = None
    ) -> None:
        async def handler(request: Request, exc: Exception) -> JSONResponse:
            return JSONResponse(
                status_code=status_code,
                content={
                    "error": err_msg,
                    "detail": err_detail if err_detail else str(exc),
                }
            )

        self.app.add_exception_handler(err, handler)