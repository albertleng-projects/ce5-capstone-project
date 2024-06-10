"""
This module contains unit tests for the logger_config module of the chatbot
application. It tests the setup_logger function to ensure it is working as
expected.

The tests are written using the unittest and pytest frameworks. The setup_logger
function in the logger_config module has corresponding test functions in
this module, which test various aspects such as the correct creation of the
logger, the creation of the logs directory, the addition of handlers to the
logger, and the correct configuration of these handlers.

Functions:
    test_setup_logger_creates_logger_with_correct_name_and_level():
      Tests if the logger is created with the correct name and level.
    test_setup_logger_creates_logs_directory_if_not_exists():
      Tests if the logs directory is created when it does not exist.
    test_setup_logger_does_not_create_logs_directory_if_exists():
      Tests if the logs directory is not created when it already exists.
    test_setup_logger_adds_two_handlers_to_logger():
      Tests if two handlers are added to the logger.
    test_setup_logger_handlers_have_correct_log_level():
      Tests if the handlers have the correct log level.
    test_setup_logger_handlers_have_correct_formatter():
      Tests if the handlers have the correct formatter.
"""

import logging
from unittest import mock
from chatbot.app import logger_config


def test_setup_logger_creates_logger_with_correct_name_and_level():
    """
    Test to verify if the setup_logger function creates a logger with the
    correct name and level.

    The function setup_logger is called with a name and level. The test asserts
    that the returned logger has the same name and level as the ones passed
    to the setup_logger function.

    This test is important to ensure that the logger is correctly set up, as the
    name and level of the logger can affect how and where the log messages
    are output.
    """
    logger = logger_config.setup_logger("test_script", logging.DEBUG)
    assert logger.name == "test_script"
    assert logger.level == logging.DEBUG


@mock.patch("os.path.exists")
@mock.patch("os.makedirs")
def test_setup_logger_creates_logs_directory_if_not_exists(mock_makedirs, mock_exists):
    """
    Test to verify if the setup_logger function creates the logs directory when
    it does not exist.

    The function setup_logger is called with a name and level. The test mocks
    the os.path.exists and os.makedirs functions to simulate a scenario where
    the logs directory does not exist. The test asserts that the os.makedirs
    function is called once with the 'logs' directory as an argument.

    This test is important to ensure that the setup_logger function correctly
    creates the logs directory when it does not exist.
    """
    mock_exists.return_value = False
    logger_config.setup_logger("test_script", logging.DEBUG)
    mock_makedirs.assert_called_once_with("logs")


@mock.patch("os.makedirs")
def test_setup_logger_does_not_create_logs_directory_if_exists(mock_makedirs):
    """
    Test to verify if the setup_logger function does not create the logs
    directory when it already exists.

    The function setup_logger is called with a name and level. The test mocks
    the os.makedirs function to simulate a scenario where the logs directory
    already exists by setting the side effect to raise a FileExistsError.
    The test asserts that the os.makedirs function is not called.

    This test is important to ensure that the setup_logger function correctly
    handles the case where the logs directory already exists and does not
    attempt to create it again.
    """
    mock_makedirs.side_effect = FileExistsError
    logger_config.setup_logger("test_script", logging.DEBUG)
    mock_makedirs.assert_not_called()


def test_setup_logger_adds_two_handlers_to_logger():
    """
    Test to verify if the setup_logger function adds two handlers to the logger.

    The function setup_logger is called with a name and level. The test first
    removes any existing handlers from the logger. Then it asserts that the
    logger has exactly two handlers after calling setup_logger, and that these
    handlers are instances of the expected classes: StreamHandler and
    TimedRotatingFileHandler.

    This test is important to ensure that the setup_logger function correctly
    sets up both a console handler and a file handler for the logger.
    """
    logger = logging.getLogger("test_script")
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    logger = logger_config.setup_logger("test_script", logging.DEBUG)
    assert len(logger.handlers) == 2
    assert isinstance(logger.handlers[0], logging.StreamHandler)
    assert isinstance(logger.handlers[1], logging.handlers.TimedRotatingFileHandler)


def test_setup_logger_handlers_have_correct_log_level():
    """
    Test to verify if the setup_logger function sets the correct log level for
    the handlers.

    The function setup_logger is called with a name and level. The test asserts
    that the log level of both handlers of the logger matches the level passed
    to the setup_logger function.

    This test is important to ensure that the setup_logger function correctly
    sets the log level for both the console handler and the file handler, as the
    log level determines which log messages are output by the handlers.
    """
    logger = logger_config.setup_logger("test_script", logging.DEBUG)
    assert logger.handlers[0].level == logging.DEBUG
    assert logger.handlers[1].level == logging.DEBUG


def test_setup_logger_handlers_have_correct_formatter():
    """
    Test to verify if the setup_logger function sets the correct formatter for
    the handlers.

    The function setup_logger is called with a name and level. The test asserts
    that both handlers of the logger have a formatter of the correct class
    (logging.Formatter), and that the format string of these formatters matches
    the expected format string.

    This test is important to ensure that the setup_logger function correctly
    sets the formatter for both the console handler and the file handler, as the
    formatter determines the format of the log messages output by the handlers.
    """
    logger = logger_config.setup_logger("test_script", logging.DEBUG)
    assert isinstance(logger.handlers[0].formatter, logging.Formatter)
    assert isinstance(logger.handlers[1].formatter, logging.Formatter)
    assert (
        logger.handlers[0].formatter._fmt
        == "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    assert (
        logger.handlers[1].formatter._fmt
        == "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
