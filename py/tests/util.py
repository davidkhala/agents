import logging

from davidkhala.utils.syntax.log import get_logger, file_handler


def prepare_logger(filename) -> logging.Logger:
    logger = get_logger('ai')
    handler = file_handler(filename)
    logger.addHandler(handler)
    return logger
