import os
from os.path import join
import glob
import shutil
import time

from config import FILE_DIR, STAGE_DIR, SKU_PRE_DIR, SKU_RAW_DIR, ASIN_PRE_DIR, ASIN_RAW_DIR


def make_dir():
    dir_list = [
        FILE_DIR, STAGE_DIR, SKU_PRE_DIR, SKU_RAW_DIR, ASIN_PRE_DIR, ASIN_RAW_DIR
    ]

    for dirs in dir_list:
        os.makedirs(dirs, exist_ok=True)


def del_residue_files():
    for each_dir in [STAGE_DIR]:
        for each_file in os.listdir(each_dir):
            os.remove(os.path.join(each_dir, each_file))


def download_wait():
    print("Waiting for downloads")
    dl_wait = True
    while dl_wait:
        time.sleep(1)
        files = os.listdir(STAGE_DIR)
        if not any(file in '.crdownload' for file in files):
            print("Downloaded!")
            dl_wait = False


def move_rename(filename, path_from, path_to):
    pattern = join(path_from, 'BusinessReport*.csv')
    files = glob.glob(pattern)
    for file_name in files:
        new_name = join(path_to, filename + '.csv')
        shutil.move(file_name, new_name)
        print(f'Moved to {path_to}')


if __name__ == '__main__':
    print(download_wait())
