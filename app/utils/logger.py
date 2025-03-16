from pathlib import PosixPath
import logging
from app.config.config import (
    LAST_HISTORY_LOGS,
    FULL_HISTORY_LOGS,
    LOG_FORMAT,
    DATETIME_FORMAT,
    log_level,
)
from app.utils.decorators.validator import validate_args
import datetime


class LoggerConfig:
    @validate_args()
    def __init__(
        self,
        logs_format: str = LOG_FORMAT,
        datetime_format: str = DATETIME_FORMAT,
        last_history_path: PosixPath = LAST_HISTORY_LOGS,
        full_history_path: PosixPath = FULL_HISTORY_LOGS,
        logs_level: str = log_level,
    ):
        self.logs_format = logs_format
        self.datetime_format = datetime_format
        self.last_history_path = last_history_path
        self.full_history_path = full_history_path
        self.logs_level = logs_level.upper()
        self.logger = logging.getLogger("my-project")
        self._setup_logger()

    def _setup_logger(self):
        self.logger.handlers.clear()
        self.logger.setLevel(self.logs_level)
        formatter = logging.Formatter(self.logs_format, self.datetime_format)
        self.logger.addHandler(self.last_run_handler(formatter))
        self.logger.addHandler(self.full_history_handler(formatter))
        self.logger.addHandler(self.console_handler(formatter))

    def last_run_handler(self, formatter: logging.Formatter) -> logging.FileHandler:
        with open(self.last_history_path, "w") as file:
            file.write(
                "=== NOWE URUCHOMIENIE ===\n"
                f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}\n"
                f"Time: {datetime.datetime.now().strftime('%H:%M:%S')}\n"
            )
        _last_run_handler = logging.FileHandler(self.last_history_path, mode="w")
        _last_run_handler.setFormatter(formatter)
        return _last_run_handler

    def full_history_handler(self, formatter: logging.Formatter) -> logging.FileHandler:
        _full_history_handler = logging.FileHandler(self.full_history_path, "a")
        _full_history_handler.setFormatter(formatter)
        return _full_history_handler

    def console_handler(self, formatter: logging.Formatter) -> logging.StreamHandler:
        _console_handler = logging.StreamHandler()
        _console_handler.setFormatter(formatter)
        return _console_handler


# Initialization logger in module
logger = LoggerConfig().logger
