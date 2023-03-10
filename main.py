from helpers import *
from base_class import Driver
from scrape import Login, Navigation
import sys

def main():

    make_dir()
    del_residue_files()
    client_list = current_client().to_dict('records')
    for item in client_list:
        driver = Driver()
        try:
            login = Login(driver, item['email'], credentials(item['name']), authentication(item['email']),
                          item['marketplace_id'])
            login.asc_login()
            navigation = Navigation(driver, item['col1'], item['col2'], item['col3'])
            navigation.navigate()
            driver.close_driver()
        except Exception as err:
            print(err)
            driver.close_driver()



if __name__ == '__main__':
    main()
