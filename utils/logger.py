import logging as _logging
from pathlib import Path as _Path

def _appendToLog(content: str, log: Logger):
    with open(log.logFile, 'a') as f:
        f.write(content + "\n")


import logging as _logging
from pathlib import Path as _Path


class Logger:
    """Wrapper around Python's logging.Logger."""

    def __init__(
        self,
        name: str | None = None,
        log_file: str | _Path | None = None,
        level: int = _logging.INFO,
        console: bool = True,
    ):
        self.logger = _logging.getLogger(name)
        self.logger.setLevel(level)

        if not self.logger.handlers:
            formatter = _logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            )

            if console:
                console_handler = _logging.StreamHandler()
                console_handler.setFormatter(formatter)
                self.logger.addHandler(console_handler)

            if log_file is not None:
                file_handler = _logging.FileHandler(
                    log_file,
                    encoding="utf-8"
                )
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self.logger.exception(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        self.logger.log(level, msg, *args, **kwargs)

    def setLevel(self, level):
        self.logger.setLevel(level)

    def addHandler(self, handler):
        self.logger.addHandler(handler)

    def removeHandler(self, handler):
        self.logger.removeHandler(handler)

    def hasHandlers(self):
        return self.logger.hasHandlers()

    def isEnabledFor(self, level):
        return self.logger.isEnabledFor(level)