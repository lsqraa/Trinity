from __future__ import annotations
import logging
import sys
from pathlib import Path

from config.settings import settings


def _setup_logger() -> logging.Logger:
    log = logging.getLogger("trinity")
    log.setLevel(logging.INFO)

    if not log.handlers:
        log_format = "[%(asctime)s] - [%(levelname)s] - %(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(fmt=log_format, datefmt=date_format)

        log_dir = Path(settings.BASE_DIR) / "data"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "trinity.log"

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)

        log.addHandler(file_handler)
        log.addHandler(stream_handler)

    return log


logger = _setup_logger()
#logger