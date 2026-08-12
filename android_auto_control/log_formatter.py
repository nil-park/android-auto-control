import logging
from collections.abc import Mapping
from typing import Any, ClassVar, Literal

from colorama import Fore, Style


class ColorFormatter(logging.Formatter):
    """A simple colored log formatter implementation.

    This formatter colorizes log level names using ANSI color codes from colorama.
    Projects should customize this according to their requirements.

    Attributes:
        base_format (str): The default log message format.
        level_colors (dict): Mapping of log levels to their display colors.
    """

    base_format = "%(levelname)s: %(message)s"

    level_colors: ClassVar[dict[int, str]] = {
        logging.DEBUG: Fore.LIGHTBLACK_EX,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.LIGHTRED_EX,
    }

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style: Literal["%", "{", "$"] = "%",
        validate: bool = True,
        *,
        defaults: Mapping[str, Any] | None = None,
    ):
        if fmt is None:
            fmt = self.base_format
        super().__init__(fmt=fmt, datefmt=datefmt, style=style, validate=validate, defaults=defaults)

    def format(self, record: logging.LogRecord) -> str:
        original_levelname = record.levelname
        level_color = self.level_colors.get(record.levelno, "")
        if level_color:
            record.levelname = f"{level_color}{record.levelname}{Style.RESET_ALL}"
        try:
            return super().format(record)
        finally:
            record.levelname = original_levelname
