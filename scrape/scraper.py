import time

from config import *
from helpers import move_rename, concat_files, header_check, del_empty_files
from datetime import datetime, timedelta




class Scraper:
    def __init__(self, driver, seller_id, marketplace_id, name, wasin, fraction,start_date,end_date):
        self.driver = driver
        self.seller_id = seller_id
        self.marketplace_id = marketplace_id
        self.name = name
        self.wasin = wasin
        self.fraction = fraction
        self.start_date = start_date
        self.end_date = end_date

    def scrape(self):
        start_date, end_date = self.start_date, self.end_date
        print(f'Downloading for date range {start_date} to {end_date}')
        filename = f'!!S!!{self.seller_id}!!S!!!!M!!{self.marketplace_id}!!M!!{self.name}!!F!!{start_date}!!F!!-!!T!!{end_date}!!T!!'
        print(filename)
        if self.marketplace_id in {'ATVPDKIKX0DER', 'A2EUQ1WTGCTBG2', 'A1AM78C64UM0Y8'}:
            self.driver.load_page('Business Report', na_br)
            self.driver.sku_download(na_sku.format(s_date=start_date, e_date=end_date), self.marketplace_id)
        else:
            self.driver.load_page('Business Report', eu_br)
            self.driver.sku_download(eu_sku.format(s_date=start_date, e_date=end_date), self.marketplace_id)
        time.sleep(5)
        move_rename(filename, STAGE_DIR, SKU_PRE_DIR)
        del_empty_files(SKU_PRE_DIR)
        header_check('SKU')
        time.sleep(15)
        if self.marketplace_id in {'ATVPDKIKX0DER', 'A2EUQ1WTGCTBG2', 'A1AM78C64UM0Y8'}:
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
        time.sleep(5)
        move_rename(filename, STAGE_DIR, ASIN_PRE_DIR)
        time.sleep(5)
        del_empty_files(ASIN_PRE_DIR)
        time.sleep(5)
        header_check('WITHOUTASIN')
        time.sleep(15)
    def fraction_download(self, url, start_date, end_date):
        while start_date <= end_date:
            print(f'Download date: {str(start_date.strftime("%Y-%m-%d"))}')
            self.driver.withoutasin_download(
                url.format(s_date=str(start_date.strftime("%Y-%m-%d")), e_date=str(start_date.strftime("%Y-%m-%d"))),
                self.marketplace_id)
            start_date = start_date + timedelta(days=1)
        concat_files()
