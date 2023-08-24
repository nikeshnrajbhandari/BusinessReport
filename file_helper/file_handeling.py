"""Handles operation in folder"""

import os
import glob
import time
import shutil
import pandas as pd
import logging

from configs.config import download_dir, stage_dir, driver_dir, log_dir, sku_pre_dir, sku_raw_dir, asin_pre_dir, \
    asin_raw_dir, SKU_HEADER, \
    WITHOUTASIN_HEADER
from error_helper.custom_error import IncorrectHeader
from os.path import join, isfile

logger = logging.getLogger("br_logger")
logger.setLevel(logging.INFO)


def dir_init():
    dir_list = [
        download_dir, driver_dir, stage_dir, log_dir, sku_pre_dir, sku_raw_dir, asin_pre_dir, asin_raw_dir
    ]
    for dirs in dir_list:
        os.makedirs(dirs, exist_ok=True)


def del_residue_files():
    for each_dir in [sku_pre_dir, asin_pre_dir]:
        for each_file in os.listdir(each_dir):
            os.remove(join(each_dir, each_file))

def del_residue_dir():
    for each_dir in [driver_dir, stage_dir]:
        shutil.rmtree(each_dir)


def download_wait(name, STAGE_DIR):
    logger.info("Waiting for downloads")
    dl_wait = True
    while dl_wait:
        time.sleep(1)
        files = os.listdir(STAGE_DIR)
        if not any(file in '.crdownload' for file in files):
            logger.info(f"[{name}] Downloaded!")
            dl_wait = False


def move_rename(filename, path_from, path_to):
    pattern = join(path_from, 'BusinessReport*.csv')
    files = glob.glob(pattern)
    for file_name in files:
        new_name = join(path_to, filename + '.csv')
        shutil.move(file_name, new_name)
        logger.info(f'Moved to {path_to}')


def concat_files(name, STAGE_DIR):
    file_format = join(STAGE_DIR, '*.csv')
    file_list = glob.glob(file_format)
    df = pd.concat(map(pd.read_csv, file_list))
    del_residue_files()
    df.to_csv(join(STAGE_DIR, 'BusinessReport.csv'), encoding='utf-8', index=False, lineterminator='\n')
    logger.info(f'[{name}] Files concat finished.')


def del_empty_files(path):
    files = [f for f in os.listdir(path) if isfile(join(path, f))]
    for file in files:
        df = pd.read_csv(join(path, file))
        if df.empty:
            logger.warning('Empty file.')
            os.remove(join(path, file))


def header_check(report_type):
    if report_type == 'SKU':
        path_from = sku_pre_dir
        header = SKU_HEADER
        path_to = sku_raw_dir
    elif report_type == 'WITHOUTASIN':
        path_from = asin_pre_dir
        header = WITHOUTASIN_HEADER
        path_to = asin_raw_dir
    files = [f for f in os.listdir(path_from) if isfile(join(path_from, f))]
    for file in files:
        df = pd.read_csv(join(path_from, file))
        column_list = list(df.columns)

        if header == column_list:
            shutil.move(join(path_from, file), join(path_to, file))
            logger.info(f"{file} moved to raw")
        elif len(header) != len(column_list) and all(item in column_list for item in header):
            df = df[header]
            logger.warning(f'Incorrect header list: {column_list}')
            df.to_csv(join(path_to, file), encoding='utf-8', index=False, lineterminator='\n')

            logger.info(f"Header Corrected for {file} [{report_type}]")
            os.remove(join(path_from, file))
        elif len(header) == len(column_list) and [item.lower() for item in column_list] == [item.lower() for item in
                                                                                            header]:
            df.columns = header
            logger.warning(f'Incorrect header list: {column_list}')
            df.to_csv(join(path_to, file), encoding='utf-8', index=False, lineterminator='\n')
            logger.info(f"Header Corrected for {file} [{report_type}]")
            os.remove(join(path_from, file))
        else:
            raise IncorrectHeader(f'Unregistered header in {report_type}')


if __name__ == '__main__':
    pass
