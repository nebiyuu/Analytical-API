# src/utils/logger.py

import logging
import os
from logging.handlers import RotatingFileHandler

def get_logger(name, log_level=None):
    """
    Returns a configured logger instance.

    Args:
        name (str): The name of the logger (usually __name__ of the calling module).
        log_level (str, optional): The logging level to set for the logger
                                   (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
                                   If None, it defaults to the LOG_LEVEL environment variable
                                   or 'INFO' if not set.

    Returns:
        logging.Logger: A configured logger instance.
    """
    # Ensure log directory exists
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Get log level from environment variable or default to INFO
    configured_log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    if log_level:
        configured_log_level = log_level.upper()

    numeric_level = getattr(logging, configured_log_level, logging.INFO)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {configured_log_level}')

    logger = logging.getLogger(name)
    logger.setLevel(numeric_level)

    # Prevent duplicate handlers if the logger is requested multiple times
    if not logger.handlers:
        # Create a console handler
        c_handler = logging.StreamHandler()
        c_handler.setLevel(numeric_level)

        # Create a file handler with rotation
        log_file_path = os.path.join(log_dir, 'app.log')
        f_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=5              # Keep up to 5 old log files
        )
        f_handler.setLevel(numeric_level)

        # Create formatters and add them to handlers
        c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

    return logger

# Example usage (for testing the logger directly)
if __name__ == "__main__":
    # Get a logger for this module
    main_logger = get_logger(__name__, log_level='DEBUG')

    main_logger.debug('This is a DEBUG message.')
    main_logger.info('This is an INFO message.')
    main_logger.warning('This is a WARNING message.')
    main_logger.error('This is an ERROR message.')
    main_logger.critical('This is a CRITICAL message.')

    # Example of another module using the logger
    another_logger = get_logger('AnotherModule')
    another_logger.info('This message is from another module.')

    # Example of setting log level via environment variable
    print("\nTesting with environment variable:")
    os.environ['LOG_LEVEL'] = 'WARNING'
    env_logger = get_logger('EnvTestLogger')
    env_logger.debug('This debug message should NOT appear (EnvTestLogger).')
    env_logger.info('This info message should NOT appear (EnvTestLogger).')
    env_logger.warning('This warning message SHOULD appear (EnvTestLogger).')
    del os.environ['LOG_LEVEL'] # Clean up environment variable for subsequent tests