"""Scrapes SKU and Without ASIN"""
import logging
import time

from base_class import Driver, DriverInit
from configs import *
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from error_helper.custom_error import NoBusinessReport
from file_helper.file_handeling import move_rename, concat_files, header_check, del_empty_files, download_wait


class Scraper(Driver):
    def __init__(self, driver: DriverInit, seller_id, marketplace_id, name, fraction, start_date, end_date, stage_dir):
        super().__init__(driver)
        self.seller_id = seller_id
        self.marketplace_id = marketplace_id
        self.name = name
        self.fraction = fraction
        self.start_date = start_date
        self.end_date = end_date
        self.logger = logging.getLogger("br_logger")
        self.logger.setLevel(logging.INFO)
        self.stage_dir = stage_dir

    def scrape(self):
        start_date, end_date = self.start_date, self.end_date
        self.logger.info(f'[{self.name}] Downloading for date range {start_date} to {end_date}')
        filename = f'!!S!!{self.seller_id}!!S!!!!M!!{self.marketplace_id}!!M!!{self.name}!!F!!{start_date}!!F!!-!!T!!{end_date}!!T!!'
        self.logger.info(filename)
        if self.marketplace_id in {'ATVPDKIKX0DER', 'A2EUQ1WTGCTBG2', 'A1AM78C64UM0Y8'}:
            self.load_page(f'[{self.name}] Business Report', na_br)
            self.sku_download(na_sku.format(s_date=start_date, e_date=end_date), self.marketplace_id)
        else:
            self.load_page(f'[{self.name}] Business Report', eu_br)
            self.sku_download(eu_sku.format(s_date=start_date, e_date=end_date), self.marketplace_id)
        time.sleep(10)
        move_rename(filename, self.stage_dir, sku_pre_dir)
        time.sleep(5)
        del_empty_files(sku_pre_dir)
        time.sleep(5)
        header_check('SKU')
        time.sleep(20)
        if self.marketplace_id in {'ATVPDKIKX0DER', 'A2EUQ1WTGCTBG2', 'A1AM78C64UM0Y8'}:
            self.load_page(f'[{self.name}] Business Report', na_br)
            if self.fraction == 0:
                self.withoutasin_download(na_asin.format(s_date=start_date, e_date=end_date),
                                          self.marketplace_id)
            elif self.fraction == 1:
                self.fraction_download(na_asin, datetime.strptime(start_date, "%Y-%m-%d"),
                                       datetime.strptime(end_date, "%Y-%m-%d"))
        else:
            self.load_page(f'[{self.name}] Business Report', eu_br)
            if self.fraction == 0:
                self.withoutasin_download(eu_asin.format(s_date=start_date, e_date=end_date),
                                          self.marketplace_id)
            elif self.fraction == 1:
                self.fraction_download(eu_asin, datetime.strptime(start_date, "%Y-%m-%d"),
                                       datetime.strptime(end_date, "%Y-%m-%d"))
        self.driver.implicitly_wait(10)
        move_rename(filename, self.stage_dir, asin_pre_dir)
        self.driver.implicitly_wait(5)
        del_empty_files(asin_pre_dir)
        self.driver.implicitly_wait(5)
        header_check('WITHOUTASIN')
        self.driver.implicitly_wait(20)

    # For clients with heavy data, which may need to be downloaded in chunks
    def fraction_download(self, url, start_date, end_date):
        while start_date <= end_date:
            self.logger.info(f'[{self.name}] Download date: {str(start_date.strftime("%Y-%m-%d"))}')
            self.withoutasin_download(
                url.format(s_date=str(start_date.strftime("%Y-%m-%d")), e_date=str(start_date.strftime("%Y-%m-%d"))),
                self.marketplace_id)
            start_date = start_date + timedelta(days=1)
        concat_files(self.name, self.stage_dir)

    def sku_download(self, url, region):
        self.load_page(f'[{self.name}] SKU', url)
        handles_before = self.driver.window_handles
        self.toggle_column()
        self.col_items(SKU_HEADER)
        if region in {'ATVPDKIKX0DER', 'A2EUQ1WTGCTBG2', 'A1AM78C64UM0Y8'}:
            if self.element_locator(na_download):
                self.btn_click(na_download)
        else:
            if self.element_locator(eu_download):
                self.btn_click(eu_download)
        self.wait_for_new_window(handles_before)
        if self.every_downloads_chrome():
            download_wait(self.name, self.stage_dir)
        self.rm_downloaded_item()

    def withoutasin_download(self, url, region):
        self.load_page(f'[{self.name}] WithoutASIN', url)
        handles_before = self.driver.window_handles
        self.toggle_column()
        self.col_items(WITHOUTASIN_HEADER)
        if region in {'ATVPDKIKX0DER', 'A2EUQ1WTGCTBG2', 'A1AM78C64UM0Y8'}:
            if self.element_locator(na_download):
                self.btn_click(na_download)
        else:
            if self.element_locator(eu_download):
                self.btn_click(eu_download)
        self.wait_for_new_window(handles_before)
        if self.every_downloads_chrome():
            download_wait(self.name, self.stage_dir)
        self.rm_downloaded_item()

    def toggle_column(self):
        if self.element_locator('//*[@id="root"]/div/div[2]/div/div[2]/div/div/kat-link') is False:
            raise NoBusinessReport(f"Can't load business report page for {self.name}")
        root1 = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[2]/div/div/kat-link')
        shadow_root1 = self.expand_shadow_element(root1)
        toggle_button = shadow_root1.find_element(By.CSS_SELECTOR, 'a')
        toggle_button.click()

    def col_items(self, col_list):
        self.element_locator('//*[@id="root"]/div/div/div/div/div/div/div/kat-checkbox')
        col_items = self.driver.find_elements(By.XPATH,
                                                     '//*[@id="root"]/div/div/div/div/div/div/div/kat-checkbox')

        for item in col_items:
            shadow_root1 = self.expand_shadow_element(item)
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
