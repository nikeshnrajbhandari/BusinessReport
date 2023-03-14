

from config import *
from helpers import date_range

from selenium.webdriver.common.by import By


class Scraper:
    def __init__(self, driver, seller_id, marketplace_id, name, wasin, fraction):
        self.driver = driver
        self.seller_id = seller_id
        self.marketplace_id = marketplace_id
        self.name = name
        self.wasin = wasin
        self.fraction = fraction

    def scrape(self):
        start_date, end_date = date_range(PULL_TYPE)
        filename = f'!!S!!{self.seller_id}!!S!!!!M!!{self.marketplace_id}!!M!!{self.name}!!F!!{start_date}!!F!!-!!T!!{end_date}!!T!!'
        print(filename)
        if self.marketplace_id == 'ATVPDKIKX0DER':
            self.driver.load_page('Business Report', na_br)
            self.driver.sku_download(na_sku.format(s_date=start_date, e_date=end_date), self.marketplace_id, filename)
        else:
            self.driver.load_page('Business Report', eu_br)

    def normal_download(self, start_date, end_date):

        self.driver.load_page('SKU', na_sku.format(s_date=start_date, e_date=end_date))
        if self.fraction == 0:
            pass
        elif self.fraction == 1:
            pass

    def fraction_download(self, start_date, end_date):

        if self.fraction == 0:
            pass
        elif self.fraction == 1:
            pass
