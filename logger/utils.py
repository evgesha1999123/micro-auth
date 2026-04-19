import inspect
import logging
import time
from datetime import datetime
from functools import wraps
from typing import (
    Any,
    Coroutine,
    Optional,
    Union,
)

import pytz  # type: ignore

LoggerType = Union[logging.Logger, logging.LoggerAdapter]
JSONType = Union[str, int, float, bool, None, list["JSONType"], dict[str, "JSONType"]]


class LocRecordDocumentMaker:
    """
    non_project_pattern: Указать строку, которая встречается в pathname LogRecord у библиотек
    """

    non_project_pattern: str = 'site-packages'
    time_zone = pytz.timezone('Europe/Moscow')

    def make_document(self, record: logging.LogRecord) -> dict[str, JSONType]:
        is_site_packages = (
            True if self.non_project_pattern in record.pathname else False
        )
        document = {
            "@timestamp": datetime.now(self.time_zone).isoformat(),
            "logger": record.name,
            "module": record.module,
            "filename": record.filename,
            "func_name": record.funcName,
            "level": record.levelname,
            "message": record.getMessage(),
            "relative_created": (
                record.relativeCreated
            ),  # время в миллисекундах, прошедшее с момента старта программы до создания этого лога
            "is_site_packages": is_site_packages,
            "extra": getattr(record, "extra", {}),
        }
        return document


def log_execution_time(logger: Optional[LoggerType] = None) -> Any:
    """
    Декоратор для логирования времени выполнения синхронных и асинхронных функций.

    Args:
        logger: Логгер или адаптер логгера для записи сообщений.
               Если не передан, будет использован корневой логгер.
    """

    def decorator(func: Any) -> Any:
        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            func_name = func.__name__
            start_time = time.perf_counter()

            result = func(*args, **kwargs)
            if isinstance(result, Coroutine):
                result = await result

            exec_time = time.perf_counter() - start_time
            message = f"Функция '{func_name}' выполнена за {exec_time:.4f} секунд"

            (logger or logging).info(message)
            return result

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            func_name = func.__name__
            start_time = time.perf_counter()

            result = func(*args, **kwargs)
            exec_time = time.perf_counter() - start_time
            message = f"Функция '{func_name}' выполнена за {exec_time:.4f} секунд"

            (logger or logging).info(message)
            return result

        if inspect.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator
