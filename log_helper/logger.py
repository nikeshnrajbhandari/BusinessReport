"""Logger using logging"""

import os
import logging
from datetime import datetime
from configs.config import log_dir


def init_logger(name):
    logger = logging.getLogger(name)

    fmt = '%(asctime)s : [%(funcName)-20s] : [%(levelname)-8s] : %(message)s'

    logging.basicConfig(level=logging.INFO, format=fmt)
    logger.setLevel(logging.INFO)

    log_file_info = f'Business_Report-{datetime.now().strftime("%Y-%m-%d")}.log'
    log_file_error = f'Business_Report-error-{datetime.now().strftime("%Y-%m-%d")}.log'

    log_file = [(log_file_info, logging.INFO), (log_file_error, logging.ERROR)]

    for file_name, level in log_file:
        file_handler = logging.FileHandler(
            filename=os.path.join(log_dir, file_name))

        formatter = logging.Formatter(fmt)

        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)

        logger.addHandler(file_handler)
    return logger
