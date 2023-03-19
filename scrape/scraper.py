from config import *
from helpers import date_range, move_rename, concat_files
from datetime import datetime, timedelta
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
        if self.marketplace_id == 'ATVPDKIKX0DER':
            self.driver.load_page('Business Report', na_br)
            self.driver.sku_download(na_sku.format(s_date=start_date, e_date=end_date), self.marketplace_id)
        else:
            self.driver.load_page('Business Report', eu_br)
            self.driver.sku_download(eu_sku.format(s_date=start_date, e_date=end_date), self.marketplace_id)
        move_rename(filename, STAGE_DIR, SKU_PRE_DIR)

        if self.marketplace_id == 'ATVPDKIKX0DER':
            self.driver.load_page('Business Report', na_br)
            if self.fraction == 0:
                if self.wasin == 'B2B':
                    self.driver.withoutasin_download(na_b2b.format(s_date=start_date, e_date=end_date),
                                                     self.marketplace_id)
                elif self.wasin == 'NOB2B':
                    self.driver.withoutasin_download(na_nob2b.format(s_date=start_date, e_date=end_date),
                                                     self.marketplace_id)
            elif self.fraction == 1:
                if self.wasin == 'B2B':
                    self.fraction_download(na_b2b, datetime.strptime(start_date, "%Y-%m-%d"),
                                           datetime.strptime(end_date, "%Y-%m-%d"))
                elif self.wasin == 'NOB2B':
                    self.fraction_download(na_nob2b, datetime.strptime(start_date, "%Y-%m-%d"),
                                           datetime.strptime(end_date, "%Y-%m-%d"))
        else:
            self.driver.load_page('Business Report', eu_br)
            if self.fraction == 0:
                if self.wasin == 'B2B':
                    self.driver.withoutasin_download(eu_b2b.format(s_date=start_date, e_date=end_date),
                                                     self.marketplace_id)
                # elif self.wasin == 'NOB2B':
                #     self.driver.withoutasin_download(na_nob2b.format(s_date=start_date, e_date=end_date),
                #                                      self.marketplace_id)
            elif self.fraction == 1:
                if self.wasin == 'B2B':
                    self.fraction_download(eu_b2b, datetime.strptime(start_date, "%Y-%m-%d"),
                                           datetime.strptime(end_date, "%Y-%m-%d"))
                # elif self.wasin == 'NOB2B':
                #     self.fraction_download(na_nob2b, datetime.strptime(start_date, "%Y-%m-%d"),
                #                            datetime.strptime(end_date, "%Y-%m-%d"))
        move_rename(filename, STAGE_DIR, ASIN_PRE_DIR)

    def fraction_download(self, url, start_date, end_date):
        while start_date <= end_date:
            print(f'Download date{str(start_date.strftime("%Y-%m-%d"))}')
            self.driver.withoutasin_download(
                url.format(s_date=str(start_date.strftime("%Y-%m-%d")), e_date=str(start_date.strftime("%Y-%m-%d"))),
                self.marketplace_id)
            start_date = start_date + timedelta(days=1)
        concat_files()
