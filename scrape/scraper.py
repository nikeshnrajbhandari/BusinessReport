import time
import logging

from config import *
from config.custom_error import NoBusinessReport
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from helpers import move_rename, concat_files, header_check, del_empty_files, download_wait


class Scraper:

    def __init__(self, driver, seller_id, marketplace_id, name, fraction, start_date, end_date):
        self.driver = driver
        self.seller_id = seller_id
        self.marketplace_id = marketplace_id
        self.name = name
        self.fraction = fraction
        self.start_date = start_date
        self.end_date = end_date
        self.logger = logging.getLogger("br_logger")
        self.logger.setLevel(logging.INFO)

    def scrape(self):
        start_date, end_date = self.start_date, self.end_date
        self.logger.info(f'Downloading for date range {start_date} to {end_date}')
        filename = f'!!S!!{self.seller_id}!!S!!!!M!!{self.marketplace_id}!!M!!{self.name}!!F!!{start_date}!!F!!-!!T!!{end_date}!!T!!'
        self.logger.info(filename)
        if self.marketplace_id in {'ATVPDKIKX0DER', 'A2EUQ1WTGCTBG2', 'A1AM78C64UM0Y8'}:
            self.driver.load_page('Business Report', na_br)
            self.sku_download(na_sku.format(s_date=start_date, e_date=end_date), self.marketplace_id)
        else:
            self.driver.load_page('Business Report', eu_br)
            self.sku_download(eu_sku.format(s_date=start_date, e_date=end_date), self.marketplace_id)
        time.sleep(5)
        move_rename(filename, STAGE_DIR, SKU_PRE_DIR)
        time.sleep(5)
        del_empty_files(SKU_PRE_DIR)
        time.sleep(5)
        header_check('SKU')
        time.sleep(5)
        if self.marketplace_id in {'ATVPDKIKX0DER', 'A2EUQ1WTGCTBG2', 'A1AM78C64UM0Y8'}:
            self.driver.load_page('Business Report', na_br)
            if self.fraction == 0:
                self.withoutasin_download(na_asin.format(s_date=start_date, e_date=end_date),
                                          self.marketplace_id)
            elif self.fraction == 1:
                self.fraction_download(na_asin, datetime.strptime(start_date, "%Y-%m-%d"),
                                       datetime.strptime(end_date, "%Y-%m-%d"))
        else:
            self.driver.load_page('Business Report', eu_br)
            if self.fraction == 0:
                self.withoutasin_download(eu_asin.format(s_date=start_date, e_date=end_date),
                                          self.marketplace_id)
            elif self.fraction == 1:
                self.fraction_download(eu_asin, datetime.strptime(start_date, "%Y-%m-%d"),
                                       datetime.strptime(end_date, "%Y-%m-%d"))
        time.sleep(5)
        move_rename(filename, STAGE_DIR, ASIN_PRE_DIR)
        time.sleep(5)
        del_empty_files(ASIN_PRE_DIR)
        time.sleep(5)
        header_check('WITHOUTASIN')
        time.sleep(5)

    def fraction_download(self, url, start_date, end_date):
        while start_date <= end_date:
            self.logger.info(f'Download date: {str(start_date.strftime("%Y-%m-%d"))}')
            self.withoutasin_download(
                url.format(s_date=str(start_date.strftime("%Y-%m-%d")), e_date=str(start_date.strftime("%Y-%m-%d"))),
                self.marketplace_id)
            start_date = start_date + timedelta(days=1)
        concat_files()

    def sku_download(self, url, region):
        self.driver.load_page('SKU', url)
        handles_before = self.driver._driver.window_handles
        self.toggle_column()
        self.col_items(SKU_HEADER)
        if region in {'ATVPDKIKX0DER', 'A2EUQ1WTGCTBG2', 'A1AM78C64UM0Y8'}:
            if self.driver.element_locator(na_download):
                self.driver.btn_click(na_download)
        else:
            if self.driver.element_locator(eu_download):
                self.driver.btn_click(eu_download)
        self.driver.wait_for_new_window(handles_before)
        if self.driver.every_downloads_chrome():
            download_wait()
        self.driver.rm_downloaded_item()

    def withoutasin_download(self, url, region):
        self.driver.load_page('WithoutASIN', url)
        handles_before = self.driver._driver.window_handles
        self.toggle_column()
        self.col_items(WITHOUTASIN_HEADER)
        if region in {'ATVPDKIKX0DER', 'A2EUQ1WTGCTBG2', 'A1AM78C64UM0Y8'}:
            if self.driver.element_locator(na_download):
                self.driver.btn_click(na_download)
        else:
            if self.driver.element_locator(eu_download):
                self.driver.btn_click(eu_download)
        self.driver.wait_for_new_window(handles_before)
        if self.driver.every_downloads_chrome():
            download_wait()
        self.driver.rm_downloaded_item()

    def toggle_column(self):
        if self.driver.element_locator('//*[@id="root"]/div/div[2]/div/div[2]/div/div/kat-link') is False:
            raise NoBusinessReport(f"Can't load business report page for {self.name}")
        root1 = self.driver._driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[2]/div/div/kat-link')
        shadow_root1 = self.driver.expand_shadow_element(root1)
        toggle_button = shadow_root1.find_element(By.CSS_SELECTOR, 'a')
        toggle_button.click()

    def col_items(self, col_list):
        self.driver.element_locator('//*[@id="root"]/div/div/div/div/div/div/div/kat-checkbox')
        col_items = self.driver._driver.find_elements(By.XPATH,
                                                      '//*[@id="root"]/div/div/div/div/div/div/div/kat-checkbox')

        for item in col_items:
            shadow_root1 = self.driver.expand_shadow_element(item)
            labels = shadow_root1.find_element(By.CSS_SELECTOR, 'kat-label')
            elements = shadow_root1.find_elements(By.CSS_SELECTOR, 'div')
            # if labels.text.upper() in col_list:
            if labels.text.upper() in [x.upper() for x in col_list]:
                if 'checkbox checked' != elements[0].get_attribute('class'):
                    try:
                        elements[0].click()
                    except Exception as err:
                        self.logger.exception(err)
            else:
                if 'checkbox checked' == elements[0].get_attribute('class'):
                    try:
                        elements[0].click()
                    except Exception as err:
                        self.logger.exception(err)
