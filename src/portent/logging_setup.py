import logging
from logging.handlers import RotatingFileHandler

from rich.logging import RichHandler


def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        handlers=[
            RichHandler(
                rich_tracebacks=True,
                show_time=False,
                show_level=True,
                show_path=False,
                markup=True,
            ),
            RotatingFileHandler("portent.log", maxBytes=1_000_000, backupCount=3),
        ],
        format="%(message)s",
    )
