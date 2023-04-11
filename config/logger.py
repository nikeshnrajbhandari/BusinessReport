import os
import logging
from config.config import BASE_DIR


def get_logger(name, log_file, level=logging.INFO):
    logger = logging.getLogger(name)
    logging.basicConfig(level=level, format='%(asctime)s :%(levelname)-8s :%(message)s')
    logger.setLevel(level)
    file_handler = logging.FileHandler(
        filename=os.path.join(BASE_DIR, 'logs', log_file))
    formatter = logging.Formatter('%(asctime)s: %(levelname)-8s: %(message)s')
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)
    return logger
