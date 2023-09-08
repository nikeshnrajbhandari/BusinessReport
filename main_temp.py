from args_helper.arguments import Argument
from pull_helper.regular_pull import RegularPull
from pull_helper.historical_pull import HistoricalPull
from helpers.client_helper import client_helper
from helpers.date_handler import DateHandler
from file_helper.custom_dir import CustomDir
from file_helper.file_reader import current_client
from log_helper.logger import init_logger
from file_helper.file_handeling import dir_init, del_residue_files, del_residue_dir

logger = init_logger('br_logger')


def folder_init():
    del_residue_files()
    del_residue_dir()
    dir_init()


def main():
    folder_init()
    argument = Argument()
    dates_obj = DateHandler(argument.pull_type())
    client_list = current_client(argument.saleforce_id())
    # print(client_list)
    if 'history' in argument.pull_type():
        # print('Feature to be implemented')
        HistoricalPull(client_list[0],dates_obj.historical_range(), CustomDir().folder_info()).pull_helper()
    else:
        chuncked_list = client_helper(client_list)
        RegularPull(chuncked_list, dates_obj.regular_range(), CustomDir().folder_info()).regular_pull()


if __name__ == '__main__':
    main()
