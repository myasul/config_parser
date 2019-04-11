import logging
import json
from logging.handlers import RotatingFileHandler

FORMATTER = logging.Formatter(
    "%(asctime)s - %(name)s- %(levelname)s- %(message)s")
LOG_FILENAME = "config_parser.log"


def get_file_handler():
    file_handler = RotatingFileHandler(
        filename=LOG_FILENAME,
        maxBytes=10485760,
        backupCount=20,
        encoding="utf8")
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(name):
    config_dict = None
    with open("../parser_logging_config.json", "r") as config_file:
        config_dict = json.load(config_file)

    if config_dict:
        logging.config.dictConfig(config_dict)
        return logging.getLogger(name)
    else:
        # Create logger from default settings
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(get_file_handler())
        logger.propagate = False

        return logger
