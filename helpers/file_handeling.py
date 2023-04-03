import os
import glob
import time
import shutil
import pandas as pd
import logging
from os.path import join, isfile
from config import FILE_DIR, STAGE_DIR, SKU_PRE_DIR, SKU_RAW_DIR, ASIN_PRE_DIR, ASIN_RAW_DIR, SKU_HEADER, \
    WITHOUTASIN_HEADER
from config.custom_error import IncorrectHeader

logger = logging.getLogger("br_logger")
logger.setLevel(logging.INFO)


def make_dir():
    dir_list = [
        FILE_DIR, STAGE_DIR, SKU_PRE_DIR, SKU_RAW_DIR, ASIN_PRE_DIR, ASIN_RAW_DIR
    ]

    for dirs in dir_list:
        os.makedirs(dirs, exist_ok=True)


def del_residue_files():
    for each_dir in [STAGE_DIR]:
        for each_file in os.listdir(each_dir):
            os.remove(join(each_dir, each_file))


def download_wait():
    logger.info("Waiting for downloads")
    dl_wait = True
    while dl_wait:
        time.sleep(1)
        files = os.listdir(STAGE_DIR)
        if not any(file in '.crdownload' for file in files):
            logger.info("Downloaded!")
            dl_wait = False


def move_rename(filename, path_from, path_to):
    pattern = join(path_from, 'BusinessReport*.csv')
    files = glob.glob(pattern)
    for file_name in files:
        new_name = join(path_to, filename + '.csv')
        shutil.move(file_name, new_name)
        logger.info(f'Moved to {path_to}')


def concat_files():
    file_format = join(STAGE_DIR, '*.csv')
    file_list = glob.glob(file_format)
    df = pd.concat(map(pd.read_csv, file_list))
    del_residue_files()
    df.to_csv(join(STAGE_DIR, 'BusinessReport.csv'), encoding='utf-8', index=False, lineterminator='\n')
    logger.info('Files concat finished.')


def del_empty_files(path):
    files = [f for f in os.listdir(path) if isfile(join(path, f))]
    for file in files:
        df = pd.read_csv(join(path, file))
        if df.empty:
            os.remove(join(path, file))


def header_check(report_type):
    # path_from = ''
    # header = []
    # path_to = ''
    if report_type == 'SKU':
        path_from = SKU_PRE_DIR
        header = SKU_HEADER
        path_to = SKU_RAW_DIR
    elif report_type == 'WITHOUTASIN':
        path_from = ASIN_PRE_DIR
        header = WITHOUTASIN_HEADER
        path_to = ASIN_RAW_DIR
    files = [f for f in os.listdir(path_from) if isfile(join(path_from, f))]
    for file in files:
        df = pd.read_csv(join(path_from, file))
        column_list = list(df.columns)
        logger.info('')
        logger.info('Header Needed.')
        logger.info('')
        logger.info(header)
        logger.info('')
        logger.info('Header in file.')
        logger.info('')
        logger.info(column_list)
        logger.info('')

        if header == column_list:
            shutil.move(join(path_from, file), join(path_to, file))
            logger.info(f"{file} moved to raw")
        elif len(header) != len(column_list) and all(item in column_list for item in header):
            df.columns = header
            logger.info('')
            logger.warning(f'Incorrect header list: {column_list}')
            logger.info('')
            df.to_csv(join(path_to, file), encoding='utf-8', index=False, lineterminator='\n')
            logger.info('')
            logger.info(f"Header Corrected for {file} [{report_type}]")
            logger.info('')
            os.remove(join(path_from, file))
        elif len(header) == len(column_list) and [item.lower() for item in column_list] == [item.lower() for item in
                                                                                            header]:
            # elif len(header) == len(column_list) and any(item in column_list for item in header):
            # elif len(header) == len(column_list):
            df.columns = header
            logger.info('')
            logger.warning(f'Incorrect header list: {column_list}')
            logger.info('')
            df.to_csv(join(path_to, file), encoding='utf-8', index=False, lineterminator='\n')
            logger.info('')
            logger.info(f"Header Corrected for {file} [{report_type}]")
            logger.info('')
            os.remove(join(path_from, file))
        else:
            raise IncorrectHeader(f'Unregistered header in {report_type}')


if __name__ == '__main__':
    header_check('WITHOUTASIN')
