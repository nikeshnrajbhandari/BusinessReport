from helpers import *
from base_class import Driver
from scrape import Login, Navigation, Scraper
import time


def main():
    make_dir()
    del_residue_files()
    client_list = current_client().to_dict('records')
    for item in client_list:
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
            time.sleep(30)
            driver.close_driver()
        except Exception as err:
            print(err)
            driver.close_driver()


if __name__ == '__main__':
    main()
