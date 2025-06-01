import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

from core.config import (
    LOG_DEBUG,
    LOG_DIR,
    LOG_FILE,
    LOG_LEVEL,
    MAX_LOG_SIZE,
    MAX_LOGS,
)


def setup_logging() -> None:
    """
    Configure logging for the application.

    This function ensures the log directory exists, rotates old log files, removes excess logs,
    and sets up a rotating file handler for the root logger. It also suppresses logging for
    noisy third-party libraries.

    Steps
    -----
    1. Ensure the log directory exists.
    2. Rotate the current log file by renaming it with a timestamp.
    3. Remove excess log files beyond the maximum allowed.
    4. Configure the root logger with a rotating file handler.
    5. Suppress logging for noisy third-party libraries.

    Notes
    -----
    If `LOG_DEBUG` is True, the logging level is set to DEBUG regardless of `LOG_LEVEL`.
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    if os.path.exists(LOG_FILE):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        rotated_name = os.path.join(LOG_DIR, f"{timestamp}.log")
        os.rename(LOG_FILE, rotated_name)

    log_files = sorted(
        [f for f in os.listdir(LOG_DIR) if f.endswith(".log")],
        key=lambda x: os.path.getmtime(os.path.join(LOG_DIR, x)),
    )
    while len(log_files) > MAX_LOGS:
        os.remove(os.path.join(LOG_DIR, log_files.pop(0)))

    logger: logging.Logger = logging.getLogger(__name__)

    # Set log level based on DEBUG and LOG_LEVEL
    if LOG_DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=MAX_LOGS
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logger.level)

    logger.addHandler(file_handler)

    for noisy_logger in [
        "httpx",
        "googleapiclient.discovery_cache",
        "werkzeug",
        "uvicorn",
        "fastapi",
    ]:
        logging.getLogger(noisy_logger).setLevel(logging.ERROR)
