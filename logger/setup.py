# logger/setup.py
import logging
import logging.config
from pathlib import Path
from typing import Optional, Union, cast

import yaml  # type: ignore[import-untyped]
from uvicorn.logging import ColourizedFormatter

logger = logging.getLogger('logger')

formatter = ColourizedFormatter(
    fmt='%(levelprefix)s %(name)-35s %(message)s', datefmt='%H:%M:%S'
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.setLevel(logging.INFO)
logger.addHandler(console_handler)


class LoggingConfigInitializer:
    config_path: Path = Path(Path(__file__).parent, 'config.yaml')

    @staticmethod
    def from_yaml(path: Path) -> dict[str, Union[str, int]]:
        """Получить конфигурацию логгера из YAML файла"""
        logger.debug(f"Создаю config для логгера из: {path}")
        with open(path, 'rt') as f:
            config = cast(dict[str, Union[str, int]], yaml.safe_load(f))
        return config

    def init(self, config: Optional[dict[str, Union[str, int]]] = None) -> None:
        if config:
            logging.config.dictConfig(config)
        else:
            logging.config.dictConfig(self.from_yaml(self.config_path))
