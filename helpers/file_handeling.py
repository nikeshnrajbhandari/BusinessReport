import os
import time

from config import FILE_DIR, STAGE_DIR, SKU_PRE_DIR, SKU_RAW_DIR, ASIN_PRE_DIR, ASIN_RAW_DIR


def make_dir():
    dir_list = [
        FILE_DIR, STAGE_DIR, SKU_PRE_DIR, SKU_RAW_DIR, ASIN_PRE_DIR, ASIN_RAW_DIR
    ]

    for dirs in dir_list:
        os.makedirs(dirs, exist_ok=True)


def del_residue_files():
    for each_dir in [SKU_PRE_DIR, ASIN_PRE_DIR]:
        for each_file in os.listdir(each_dir):
            os.remove(os.path.join(each_dir, each_file))


def download_wait(directory, timeout, nfiles=None):
    """
    Wait for downloads to finish with a specified timeout.

    Args
    ----
    directory : str
        The path to the folder where the files will be downloaded.
    timeout : int
        How many seconds to wait until timing out.
    nfiles : int, defaults to None
        If provided, also wait for the expected number of files.

    """
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < timeout:
        time.sleep(1)
        dl_wait = False
        files = os.listdir(directory)
        if nfiles and len(files) != nfiles:
            dl_wait = True

        for fname in files:
            if fname.endswith('.crdownload'):
                dl_wait = True

        seconds += 1
    return seconds
