import os
import time
import pandas as pd

from datetime import datetime
from base_class import Driver
from config.logger import get_logger
from config import PULL_TYPE, headless
from scrape import Login, Navigation, Scraper
from config.custom_error import NoBusinessReport
from helpers import make_dir, del_residue_files, date_range, current_client, credentials, authentication

logger = get_logger('br_logger', f'Business_Report-{datetime.now().strftime("%Y-%m-%d")}.log')


def main():
    dates = list()
    make_dir()
    del_residue_files()
    if PULL_TYPE.lower() in ['weekly', 'monthly', 'monthly_history', 'weekly_history']:
        dates = date_range(PULL_TYPE)

    if os.path.isfile('config_file/Failed_File.csv'):
        os.remove('config_file/Failed_File.csv')
    client_list = current_client()
    br_download(client_list, dates)
    logger.info('Download process completed!')


def br_download(client_list, dates, count=0):
    failed = []
    for item in client_list:

        if item['active'] == 1:
            driver = Driver(headless)
            logger.info(item)
            try:
                login = Login(driver, item['email'], credentials(item['name']), authentication(item['email']),
                              item['marketplace_id'])
                login.asc_login()
                navigation = Navigation(driver, item['col1'], item['col2'], item['col3'])
                navigation.navigate()
                # logger.info(dates)
                for date in dates:
                    scraper = Scraper(driver, item['seller_id'], item['marketplace_id'], item['name'], item['fraction'],
                                      date[0], date[1])
                    scraper.scrape()
                logger.info(f"Download complete for {item['name']}")
                time.sleep(5)
            except NoBusinessReport as err:
                logger.error(err)
            except Exception as err:
                logger.error(f"Failed to download for {item['name']}")
                logger.exception(err)
                failed.append(item)
            finally:
                try:
                    driver.close_driver()
                except Exception as err:
                    logger.exception(err)
                    pass
    if len(failed) > 0 and count < 3:
        time.sleep(1800)
        logger.info(f'Retry count: {count + 1}')
        br_download(failed, dates, count + 1)
    elif len(failed) > 0:
        failed_file = pd.DataFrame(failed)
        failed_file.to_csv(os.path.join('config_file', f'Failed_File-{datetime.now().strftime("%Y-%m-%d")}.csv'),
                           index=False, lineterminator='\n')


if __name__ == '__main__':
    main()
