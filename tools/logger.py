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
        mode='a+',
        encoding="utf8")
    file_handler.setFormatter(FORMATTER)
    return file_handler


def create_log_file():
    # Create folder where the parsed csvs would be stored
    log_dir = "{}/log".format(os.getcwd())
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
        config_file = open(log_dir + "/config_parser.log", "w+")
        config_file.close()
    elif not os.path.exists(log_dir + "/config_parser.log"):
        config_file = open(log_dir + "/config_parser.log", "w+")
        config_file.close()


def get_logger(name):
    create_log_file()

    dir = os.path.dirname(__file__)
    config_dict = None
    config_file_path = os.path.join(dir, "../parser_logging_config.json")

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
