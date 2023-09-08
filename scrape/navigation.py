"""Custom made foe Seller central navigation page"""
import logging

from base_class import Driver, DriverInit
from configs import *


class Navigation(Driver):

    def __init__(self, driver: DriverInit, name, col1, col2, col3):
        super().__init__(driver)
        self.name = name
        self.columns = [col1, col2, col3]
        self.logger = logging.getLogger("br_logger")
        self.logger.setLevel(logging.INFO)

    def navigate(self):
        column_list = [[col1_xpath, self.columns[0]],
                       [col2_xpath, self.columns[1]],
                       [col3_xpath, self.columns[2]]]

        try:
            self.load_page(self.name, 'Navigation')
            for items in column_list:
                self.selector(items[0], items[1])
        except Exception:
            if self.element_locator(self.name, home_xpath) is False:
                self.logger.error(f'[{self.name}] Navigation Page not found.')
                raise

    def selector(self, xpath, name_column):
        self.column_element_finder(self.name, xpath, name_column)
        self.btn_click(self.name, nav_submit_btn_xpath)
