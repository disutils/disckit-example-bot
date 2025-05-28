"""
This module provides a utility function for setting up logging in the application.

Functions:
----------
- setup_logging() -> None:
    Configures logging with a rotating file handler, manages log file rotation, and suppresses noisy loggers.

Constants:
----------
- LOG_DIR: Directory where log files are stored.
- LOG_FILE: Name of the main log file.
- MAX_LOG_SIZE: Maximum size of a single log file (in bytes).
- MAX_LOGS: Maximum number of log files to retain.
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

from core.config import LOG_DIR, LOG_FILE, MAX_LOG_SIZE, MAX_LOGS


def setup_logging() -> None:
    """
    Configures logging for the application.

    This function sets up a rotating file handler for logging, ensures the log directory exists,
    rotates old log files, and suppresses noisy loggers.

    Steps:
    ------
    1. Create the log directory if it doesn't exist.
    2. Rotate the current log file by renaming it with a timestamp.
    3. Remove excess log files beyond the maximum allowed.
    4. Configure the root logger with a rotating file handler.
    5. Suppress logging for noisy third-party libraries.
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
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=MAX_LOGS
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)

    for noisy_logger in [
        "httpx",
        "googleapiclient.discovery_cache",
        "werkzeug",
        "uvicorn",
        "fastapi",
    ]:
        logging.getLogger(noisy_logger).setLevel(logging.ERROR)
