import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--client', required=False)
    parser.add_argument('-p', '--report_type', required=True, type=str)
    return parser.parse_args()
