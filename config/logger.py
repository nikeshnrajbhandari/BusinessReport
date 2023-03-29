import os
import logging
from datetime import datetime
from config.config import BASE_DIR


def get_logger(name):
    logger = logging.getLogger(name)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s :%(levelname)-8s :%(message)s')
    logger.setLevel(logging.INFO)
    return logger
def create_log():
    file_handler = logging.FileHandler(
        filename=os.path.join(BASE_DIR, 'logs', f'Business_Report-{datetime.now().strftime("%Y-%m-%d")}.log'))
    formatter = logging.Formatter('%(asctime)s: %(levelname)-8s: %(message)s')
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)

# def console_print():
#     console = logging.StreamHandler()
#     logging.getLogger().addHandler(console)

