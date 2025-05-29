"""
This module provides a utility function for setting up logging in the application.

Functions:
----------
- setup_logging() -> None:
    Configures logging with a rotating file handler, manages log file rotation, and suppresses noisy loggers.

Constants:
----------
- LOG_DIR: The directory where log files are stored.
- LOG_FILE: The name of the main log file.
- MAX_LOG_SIZE: The maximum size of a single log file (in bytes).
- MAX_LOGS: The maximum number of log files to retain.
- LOG_LEVEL: The logging level for the application.
- DEBUG: A flag to enable or disable debug mode.
"""

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
    Configures logging for the application.

    This function performs the following steps:
    1. Ensures the log directory exists.
    2. Rotates the current log file by renaming it with a timestamp.
    3. Removes excess log files beyond the maximum allowed.
    4. Configures the root logger with a rotating file handler.
    5. Suppresses logging for noisy third-party libraries.

    If DEBUG is True, the logging level is set to DEBUG regardless of LOG_LEVEL.
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

    logger = logging.getLogger()

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
