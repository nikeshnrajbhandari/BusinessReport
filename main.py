"""Testing multithreading producer_consumer"""

import os
import time
import pandas as pd

from queue import Queue
from random import randint
from threading import Thread
from base_class import Driver
from datetime import datetime
from threading import Barrier
from helpers.logger import get_logger
from config import PULL_TYPE, headless, FILE_DIR, join
from scrape import Login, Navigation, Scraper
from config.custom_error import NoBusinessReport
from helpers import make_dir, del_residue_files, date_range, current_client, credentials, authentication

logger = get_logger('br_logger')


def main():
    global failed
    failed = []
    dates = list()
    make_dir()
    del_residue_files()

    if PULL_TYPE.lower() in ['weekly', 'monthly', 'monthly_history', 'weekly_history']:
        dates = date_range(PULL_TYPE)

    if os.path.isfile('config_file/Failed_File.csv'):
        os.remove('config_file/Failed_File.csv')

    client_list = current_client()
    n_process = 4
    chunked_list = [client_list[i::4] for i in range(4)]
    folders = ['stage1', 'stage2', 'stage3', 'stage4']

    queue = Queue()
    barrier = Barrier(n_process)

    count = 0

    # Producer-Consumer Implementation, will retry if there are failed files.
    while count < 3:
        try:
            if len(failed) != 0:
                time.sleep(800)
                logger.info('Resuming for failed files.')
                chunked_list = [failed[i::4] for i in range(4)]
        finally:
            consumers = [Thread(target=consumer, args=(queue, dates, folder,)) for folder in folders]

            producers = [Thread(target=producer, args=(barrier, queue, chunks, randint(0, 30))) for chunks in
                         chunked_list]

            for threads in producers:
                threads.start()
            for threads in consumers:
                threads.start()

            for threads in producers:
                threads.join()
            for threads in consumers:
                threads.join()
            count = count + 1

    if len(failed) > 0:
        failed_file = pd.DataFrame(failed)
        failed_file.to_csv(os.path.join('config_file', f'Failed_File-{datetime.now().strftime("%Y-%m-%d")}.csv'),
                           index=False, lineterminator='\n')

    logger.info('Download process completed!')
    for folder in folders:
        try:
            os.remove(join(FILE_DIR, folder))
        except PermissionError:
            print(f'{join(FILE_DIR, folder)}: File/Folder in use')
    quit()


def producer(barrier, queue, clients, identifier):
    # Producer, puts a client into share buffer, and uses barrier and will close the producer
    logger.info(f'Producer {identifier}: Running')
    if len(clients) != 0:
        for client in clients:
            queue.put(client)
    barrier.wait()
    queue.put(None)
    logger.info(f'Producer {identifier}: Done')


def consumer(queue, dates, folder):
    # Consumer, Will create stage directories, and get client from shared buffer to download
    logger.info(f'Consumer {folder}: Running')
    stage_dir = join(FILE_DIR, folder)
    os.makedirs(stage_dir, exist_ok=True)
    while True:
        item = queue.get()
        # Checks if there shared buffer is empty, and closes the queue if None.
        if item is None:
            queue.put(item)
            break
        logger.info(f'Consumer {folder} got :{item}')
        try:
            br_download(item, dates, stage_dir)
        except Exception as err:
            logger.error(err)
        finally:
            # Clears the stage directory
            for each_file in os.listdir(stage_dir):
                os.remove(join(stage_dir, each_file))
    logger.info(f'Consumer {folder}: Done')


def br_download(item, dates, folder):
    # Business Report scraping
    if item['active'] == 1:
        driver = Driver(folder, headless)
        try:
            login = Login(driver, item['email'], credentials(item['name']), authentication(item['email']),
                          item['marketplace_id'])
            login.asc_login()
            navigation = Navigation(driver, item['col1'], item['col2'], item['col3'])
            navigation.navigate()
            for date in dates:
                scraper = Scraper(driver, item['seller_id'], item['marketplace_id'], item['name'], item['fraction'],
                                  date[0], date[1], folder)
                scraper.scrape()
            logger.info(f"Download complete for {item['name']}")
            time.sleep(5)
        except NoBusinessReport as err:
            # When there is no business report section, will not flag as failed.
            print(err)
        except Exception as err:
            logger.error(f"Failed to download for {item['name']}")
            logger.exception(err)
            failed.append(item)
            pass
        finally:
            try:
                driver.close_driver()
            except Exception as err:
                logger.exception(err)
                pass


if __name__ == '__main__':
    main()
