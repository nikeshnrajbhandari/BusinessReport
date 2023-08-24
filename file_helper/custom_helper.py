from os.path import dirname, abspath, join
from pathlib import Path


def project_dir():
    return dirname(dirname(dirname(abspath(__file__))))


def doc_dir():
    return join(str(Path.home()), 'Documents', 'BusinessReport')


def download_dir():
    return join(doc_dir(), 'BusinessReport')


def stage_dir():
    return join(download_dir(), 'Stage')


def driver_dir():
    return join(doc_dir(), 'Webdriver')


def log_dir():
    return join(doc_dir(), 'BR_logs')


def join_dir(base, folder):
    return join(base, folder)


if __name__ == '__main__':
    print(project_dir())
