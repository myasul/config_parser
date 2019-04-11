import logging
import logging.config
import json
import os
from logging.handlers import RotatingFileHandler

FORMATTER = logging.Formatter(
    "%(asctime)s - %(name)s- %(levelname)s- %(message)s")
LOG_FILENAME = "log/config_parser.log"


def get_file_handler():
    file_handler = RotatingFileHandler(
        filename=LOG_FILENAME,
        maxBytes=10485760,
        backupCount=20,
        encoding="utf8")
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(name):
    dir = os.path.dirname(__file__)
    config_file_path = os.path.join(dir, "../parser_logging_config.json")
    config_dict = None

    with open(config_file_path, "r") as config_file:
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
