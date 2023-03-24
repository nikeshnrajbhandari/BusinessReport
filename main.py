import os
import time
import pandas as pd
from config import PULL_TYPE, headless
from helpers import *
from base_class import Driver
from scrape import Login, Navigation, Scraper


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
    print('Download complete for all clients!')


def br_download(client_list, dates, count=0):
    failed = []
    for item in client_list:

        if item['active'] == 1:

            driver = Driver(headless)
            print(item)
            try:
                login = Login(driver, item['email'], credentials(item['name']), authentication(item['email']),
                              item['marketplace_id'])
                login.asc_login()
                navigation = Navigation(driver, item['col1'], item['col2'], item['col3'])
                navigation.navigate()
                print(dates)
                for date in dates:
                    scraper = Scraper(driver, item['seller_id'], item['marketplace_id'], item['name'],
                                      item['wasin'], item['fraction'], date[0], date[1])
                    scraper.scrape()
                print(f"Download complete for {item['name']}")
                time.sleep(5)
                driver.close_driver()
            except Exception as err:
                print('Failed to download')
                print(err)
                failed.append(item)
            finally:
                try:
                    driver.close_driver()
                except Exception:
                    pass
    if len(failed) > 0 and count < 5:
        print(f'Retry count: {count + 1}')
        br_download(failed, dates, count + 1)
    elif len(failed) > 0:
        failed_file = pd.DataFrame(failed)
        failed_file.to_csv(os.path.join('config_file', 'Failed_File.csv'), index=False, lineterminator='\n')


if __name__ == '__main__':
    main()
