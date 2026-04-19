import asyncio
import logging
from abc import ABC, abstractmethod
from asyncio import Queue, Task
from logging import Handler
from typing import Optional

from .setup import logger


class BaseAsyncHandler(Handler, ABC):
    """Базовый асинхронный хендлер для логов"""

    def __init__(self) -> None:
        super().__init__()
        self._queue: Queue = asyncio.Queue()
        self.__worker_task: Optional[Task] = None  # Пока не создаём задачу

    async def _ensure_worker(self) -> None:
        """Создаёт задачу, если её ещё нет"""
        if self.__worker_task is None:
            self.__worker_task = asyncio.create_task(self._background_worker())

    async def _background_worker(self) -> None:
        """Фоновая задача для обработки логов"""
        while True:
            try:
                record = await self._queue.get()
                await self.task(record)
            except Exception as e:
                logger.exception(e)

    @abstractmethod
    async def task(self, record: logging.LogRecord) -> None:
        """Асинхронная задача"""

    @abstractmethod
    def sync_task(self, record: logging.LogRecord) -> None:
        """Синхронная задача"""

    def emit(self, record: logging.LogRecord) -> None:
        """Добавляем запись в очередь (синхронный метод)"""
        try:
            loop = asyncio.get_running_loop()  # Получаем работающий event loop
            loop.create_task(self._ensure_worker())  # Запускаем воркер, если его нет
            loop.create_task(self._queue.put(record))  # Кладём запись в очередь
        except RuntimeError:
            logger.debug(
                'Асинхронного контекста пока нет, сообщение'
                f' "{record.getMessage()[:20]}..." обработано хэндлером:'
                f' {self.__class__.__name__} в синхронном режиме'
            )
            self.sync_task(record)
