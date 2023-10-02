"""Testing multithreading producer_consumer"""

import os
import sys
import time
import pandas as pd
from file_helper.file_reader import current_client, credentials, authentication
from queue import Queue
from random import randint
from threading import Thread
from base_class import Driver
from datetime import datetime
from threading import Barrier
from logs.logger import init_logger
from scrape import Login, Navigation, Scraper
from error_helper.custom_error import NoBusinessReport
from config import PULL_TYPE, headless, FILE_DIR, join
# from webdriver_manager.chrome import ChromeDriverManager
from file_helper.file_handeling import make_download_dir, del_residue_files
from helpers import date_range

logger = init_logger('br_logger')


def main():
    # driver_path = ChromeDriverManager().install()

    global failed
    failed = []
    dates = list()
    make_download_dir()
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
                logger.info(failed)
                logger.info('Waiting for failed files.')
                time.sleep(180)
                logger.info('Resuming for failed files.')
                chunked_list = [failed[i::4] for i in range(4)]
        finally:
            consumers = [Thread(target=consumer, args=(queue, dates, folder, f'driver_{folder}')) for folder in folders]

            producers = [Thread(target=producer, args=(barrier, queue, chunks, randint(0, 30))) for chunks in
                         chunked_list]

            for threads in consumers:
                threads.start()

            for threads in producers:
                threads.start()
            # producers[0].start()
            # consumers[0].start()

            for threads in producers:
                threads.join()
            # producers[0].join()
            # consumers[0].join()
            for threads in consumers:
                threads.join()
            count = count + 1

    if len(failed) > 0:
        failed_file = pd.DataFrame(failed)
        failed_file.to_csv(os.path.join('failed_file', f'Failed_File-{datetime.now().strftime("%Y-%m-%d")}.csv'),
                           index=False, lineterminator='\n')

    logger.info('Download process completed!')
    sys.exit('Download process completed!')


def producer(barrier, queue, clients, identifier):
    # Producer, puts a client into share buffer, and uses barrier and will close the producer
    logger.info(f'Producer {identifier}: Running')
    if len(clients) != 0:
        for client in clients:
            queue.put(client)
    barrier.wait()
    queue.put(None)
    logger.info(f'Producer {identifier}: Done')


def consumer(queue, dates, folder, driver_folder):
    # Consumer, Will create stage directories, and get client from shared buffer to download
    logger.info(f'Consumer {folder}: Running')
    stage_dir = join(FILE_DIR, folder)
    driver_dir = join(FILE_DIR,driver_folder)
    os.makedirs(stage_dir, exist_ok=True)
    os.makedirs(driver_dir, exist_ok=True)
    while True:
        item = queue.get()
        # Checks if there shared buffer is empty, and closes the queue if None.
        if item is None:
            queue.put(item)
            break
        logger.info(f'Consumer {folder} got :{item}')
        try:
            br_download(item, dates, stage_dir, driver_dir)
        except Exception as err:
            logger.exception(err)
        finally:
            # Clears the stage directory
            for each_file in os.listdir(stage_dir):
                os.remove(join(stage_dir, each_file))
    logger.info(f'Consumer {folder}: Done')


def br_download(item, dates, folder, driver_dir):
    # Business Report scraping
    if item['active'] == 1:
        driver = Driver(folder,driver_dir, headless)
        try:
            login = Login(driver, item['email'], credentials(item['name']), authentication(item['email']),
                          item['marketplace_id'])
            login.asc_login()

            navigation = Navigation(driver, item['col1'], item['col2'], item['col3'])
            navigation.navigate()
            for date in dates:
                parameters = {
                    "driver": driver,
                    "seller_id": item['seller_id'],
                    "marketplace_id": item['marketplace_id'],
                    "name": item['name'],
                    "fraction": item['fraction'],
                    "start_date": date[0],
                    "end_date": date[1],
                    "STAGE_DIR": folder
                }
                scraper = Scraper(**parameters)
                scraper.scrape()
            logger.info(f"Download complete for {item['name']}")
            time.sleep(5)
        except NoBusinessReport as err:
            # When there is no business report section, will not flag as failed.
            logger.exception(err)
        except Exception as err:
            logger.error(f"Failed to download for {item['name']}")
            logger.exception(err)
            failed.append(item)


if __name__ == '__main__':
    main()
