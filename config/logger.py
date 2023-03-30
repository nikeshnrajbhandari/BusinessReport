import os
import logging
from datetime import datetime
from config.config import BASE_DIR


def get_logger(name, log_file, level=logging.INFO):
    file_handler = logging.FileHandler(
        filename=os.path.join(BASE_DIR, 'logs', log_file))
    formatter = logging.Formatter('%(asctime)s: %(levelname)-8s: %(message)s')
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    # logging.basicConfig(level=logging.INFO, format='%(asctime)s :%(levelname)-8s :%(message)s')
    logger.setLevel(level)
    logging.getLogger().addHandler(file_handler)

    # console = logging.StreamHandler()
    # logging.getLogger().addHandler(console)
    return logger

