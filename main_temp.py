from args_helper.arguments import Argument
from pull_helper.regular_pull import RegularPull
from helpers.client_helper import client_helper
from helpers.date_handler import DateHandler
from file_helper.custom_dir import CustomDir
from file_helper.file_reader import current_client
from log_helper.logger import init_logger

logger = init_logger('br_logger')
def main():
    argument = Argument()
    client_list = current_client(argument.saleforce_id())
    chuncked_list = client_helper(client_list)
    dates_obj = DateHandler(argument.pull_type())
    if 'history' in argument.pull_type():
        print('Feature to be implemented')
    else:
        RegularPull(chuncked_list, dates_obj.regular_range(), CustomDir().folder_info()).regular_pull()


if __name__ == '__main__':
    main()
