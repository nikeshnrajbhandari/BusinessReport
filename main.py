from helpers import *
import pandas as pd
from base_class import Selenium
from scrape import Login


def main():
    make_dir()
    del_residue_files()
    client_list = current_client().to_dict('records')
    for item in client_list:
        print(item['email'])
        creds = credentials(item['name'])
        otp = authentication(item['email'])
        login = Login(item['email'],creds,otp)
        login.asc_login()
        # login.sign_in()
        # login.authentication()


if __name__ == '__main__':
    main()
