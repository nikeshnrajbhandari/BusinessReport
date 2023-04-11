import argparse
from argparse import RawTextHelpFormatter


def get_args():
    parser = argparse.ArgumentParser(description='Business Report', formatter_class=RawTextHelpFormatter)
    parser.add_argument('-c', '--client', required=False, help='Enter a salesforce ID [Default: All]')
    parser.add_argument('-p', '--report_type', required=True, type=str,
                        help='''\
    Select a specific report[Required]:
    -weekly,
    -monthly, 
    -monthly_history,
    -weekly_history
    ''')

    return parser.parse_args()
