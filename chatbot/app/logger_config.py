"""
This module contains the setup_logger function which is used to configure
the logger for the application.

The setup_logger function takes in a script name and a logging level, and sets
up a logger with a console handler and a file handler. The file handler writes
logs to a file in a 'logs' directory, and rotates the log file at midnight
every day, keeping a backup of the last 14 days. The console handler writes logs
to the console.

Both handlers use a formatter that includes the time of logging, the name of
the logger, the logging level, and the log message.

Functions:
    setup_logger(script_name: str, logging_level: int) -> logging.Logger:
    Sets up and returns a logger with the given name and logging level.
"""

import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime


def setup_logger(
    script_name: str, logging_level: int = logging.DEBUG
) -> logging.Logger:
    """
    Sets up and returns a logger with the given name and logging level.

    This function creates a logger with the provided script name and logging
    level. It sets up a console handler and a file handler for the logger.
    The file handler writes logs to a file in a 'logs' directory, and rotates
    the log file at midnight every day, keeping a backup of the last 14 days.
    The console handler writes logs to the console.

    Both handlers use a formatter that includes the time of logging, the name of
    the logger, the logging level, and the log message.

    Args:
        script_name (str): The name of the script where the logger is being set up.
        logging_level (int): The logging level to be set for the logger.

    Returns:
        logging.Logger: The configured logger.
    """
    logger = logging.getLogger(script_name)
    logger.setLevel(logging_level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_level)

    if not os.path.exists("logs"):
        os.makedirs("logs")
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_handler = TimedRotatingFileHandler(
        f"logs/{script_name}_{current_time}.log", when="midnight", backupCount=14
    )
    file_handler.setLevel(logging_level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
