"""Arguments list"""
import argparse
import logging
import sys

from argparse import RawTextHelpFormatter


def get_args():
    parser = argparse.ArgumentParser(description='Business Report', formatter_class=RawTextHelpFormatter)
    parser.add_argument('-c', '--client', required=False, help='Enter a salesforce ID [Default: All]')
    parser.add_argument('-m', '--marketplace_id', required=False, help='Enter a Marketplace ID [Default: All]')
    parser.add_argument('-p', '--report_type', required=True, type=str,
                        help='''\
    Select a specific report[Required]:
    -weekly,
    -monthly, 
    -monthly_history,
    -weekly_history
    ''')

    return parser.parse_args()


# Argument
class Argument:
    def __init__(self,):
        self.args = get_args()
        self.logger = logging.getLogger("br_logger")
        self.logger.setLevel(logging.INFO)
    def salesforce_id(self):
        return self.args.client
    def marketplace_id(self):
        return self.args.marketplace_id
    def pull_type(self):
        if self.args.report_type in ('monthly_history','weekly_history')  and self.salesforce_id() is None:
            self.logger.warning("Select a specific client for historical pull")
            sys.exit("Process exited as there is no client defined.")
        return self.args.report_type
