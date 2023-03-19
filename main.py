from helpers import *
from base_class import Driver
from scrape import Login, Navigation, Scraper
import time
import pandas as pd

def main():
    make_dir()
    del_residue_files()
    df_failed = pd.DataFrame()
    client_list = current_client().to_dict('records')
    for item in client_list:
        if item['active'] == 1:
            driver = Driver()
            print(item)
            try:
                login = Login(driver, item['email'], credentials(item['name']), authentication(item['email']),
                              item['marketplace_id'])
                login.asc_login()
                navigation = Navigation(driver, item['col1'], item['col2'], item['col3'])
                navigation.navigate()
                scraper = Scraper(driver, item['seller_id'], item['marketplace_id'], item['name'],
                                  item['wasin'], item['fraction'])
                scraper.scrape()
                time.sleep(5)
                driver.close_driver()
            except Exception as err:
                print(err)
                driver.close_driver()
                df_dictionary = pd.DataFrame(item)
                df_failed = pd.concat(df_failed, df_dictionary, ignore_index=True)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df_failed)


if __name__ == '__main__':
    main()
