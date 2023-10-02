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
        self.marketplaces = ('ATVPDKIKX0DER', 'A2EUQ1WTGCTBG2', 'A1AM78C64UM0Y8')
        self.date_format = "%Y-%m-%d"
        self.logger = logging.getLogger("br_logger")
        self.logger.setLevel(logging.INFO)
        self.stage_dir = stage_dir

    def scrape(self):
        dtype_params = {
            'sku': {'na': {'url': na_br, 'br': na_sku}, 'eu': {'url': eu_br, 'br': eu_sku}, 'pre': sku_pre_dir},
            'asin': {'na': {'url': na_br, 'br': na_asin}, 'eu': {'url': eu_br, 'br': eu_asin}, 'pre': asin_pre_dir}
        }
        self.logger.info(f'[{self.name}] Downloading for date range {self.start_date} to {self.end_date}')
        filename = f'!!S!!{self.seller_id}!!S!!!!M!!{self.marketplace_id}!!M!!{self.name}!!F!!{self.start_date}!!F!!-!!T!!{self.end_date}!!T!!'
        # self.logger.info(filename)
        if self.marketplace_id in self.marketplaces:
            region = 'na'
        else:
            region = 'eu'

        for key in dtype_params:
            self.load_page(self.name, 'Business Report', dtype_params[key][region].get('url'))
            if key == 'asin' and self.fraction == 1:
                self.fraction_download(url=dtype_params[key][region].get('br'),
                                       start_date=datetime.strptime(self.start_date, self.date_format),
                                       end_date=datetime.strptime(self.end_date, self.date_format),
                                       region=region,
                                       report=key)
            else:
                self.download(
                    url=dtype_params[key][region].get('br').format(s_date=self.start_date, e_date=self.end_date),
                    region=region, report=key)

            self.driver.implicitly_wait(10)
            # move_rename(self.name, filename, self.stage_dir, dtype_params[key].get('pre'))
            move_rename(self.name, filename, self.stage_dir, self.stage_dir)
            # self.driver.implicitly_wait(5)
            # del_empty_files(self.name, dtype_params[key].get('pre'))
            self.driver.implicitly_wait(5)
            header_check(self.name, key, self.stage_dir)
            self.driver.implicitly_wait(20)

    # For clients with heavy data, which may need to be downloaded in chunks
    def fraction_download(self, url, start_date, end_date, region, report):
        while start_date <= end_date:
            self.logger.info(f'[{self.name}] Download date: {str(start_date.strftime(self.date_format))}')
            self.download(
                url=url.format(s_date=str(start_date.strftime(self.date_format)),
                               e_date=str(start_date.strftime(self.date_format))),
                region=region,
                report=report
            )
            start_date = start_date + timedelta(days=1)
        concat_files(self.name, self.stage_dir)

    def download(self, url, region, report):
        self.load_page(self.name, report.upper(), url)
        handles_before = self.driver.window_handles
        self.toggle_column()

        if report == 'sku':
            header = SKU_HEADER
        elif report == 'asin':
            header = WITHOUTASIN_HEADER
        self.col_items(header)

        download_param = {'na': na_download, 'eu': eu_download}

        if self.element_locator(self.name, download_param.get(region)):
            self.btn_click(self.name, download_param.get(region))

        self.wait_for_new_window(handles_before)
        if self.every_downloads_chrome():
            download_wait(self.name, report.upper(), self.stage_dir)
        self.rm_downloaded_item(self.name)

    def toggle_column(self):
        if self.element_locator(self.name, '//*[@id="root"]/div/div[2]/div/div[2]/div/div/kat-link') is False:
            raise NoBusinessReport(f"Can't load business report page for {self.name}")
        root1 = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[2]/div/div/kat-link')
        shadow_root1 = self.expand_shadow_element(root1)
        toggle_button = shadow_root1.find_element(By.CSS_SELECTOR, 'a')
        toggle_button.click()

    def col_items(self, col_list):
        self.element_locator(self.name, '//*[@id="root"]/div/div/div/div/div/div/div/kat-checkbox')
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
                    except Exception:
                        raise
            else:
                if 'checkbox checked' == elements[0].get_attribute('class'):
                    try:
                        elements[0].click()
                    except Exception:
                        raise
