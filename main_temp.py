import sys
import shutil
import os
from os.path import join
from args_helper.arguments import Argument
from pull_helper.regular_pull import RegularPull
from pull_helper.historical_pull import HistoricalPull
from helpers.client_helper import client_helper
from helpers.date_handler import DateHandler
from file_helper.custom_dir import CustomDir
from file_helper.file_reader import current_client
from log_helper.logger import init_logger
from file_helper.file_handeling import dir_init, del_residue_files, del_residue_stage_files, del_residue_dir, sku_pre_dir, sku_raw_dir, \
    asin_pre_dir, asin_raw_dir

logger = init_logger('br_logger')


def folder_clean():
    del_residue_files()

def move_to_raw(name, pre_dir, raw_dir):
    for each_file in os.listdir(pre_dir):
        shutil.move(join(pre_dir, each_file), join(raw_dir, each_file))
    logger.info(f'Moved {name} from pre to raw')


def main():
    folder_clean()
    dir_init()
    argument = Argument()
    dates_obj = DateHandler(argument.pull_type())
    client_list = current_client(argument.salesforce_id())
    # print(client_list)
    if 'history' in argument.pull_type():
        # print('Feature to be implemented')
        HistoricalPull(client_list[0], dates_obj.historical_range(), CustomDir().folder_info()).pull_helper()
    else:
        chuncked_list = client_helper(client_list)
        RegularPull(chuncked_list, dates_obj.regular_range(), CustomDir().folder_info()).regular_pull()
    move_to_raw('SKU',sku_pre_dir, sku_raw_dir)
    move_to_raw('ASIN',asin_pre_dir, asin_raw_dir)
    sys.exit('Process Completed.')



if __name__ == '__main__':
    main()
