import logging

from config import *


class Navigation:

    def __init__(self, driver, col1, col2, col3):
        self.driver = driver
        self.columns = [col1, col2, col3]
        self.logger = logging.getLogger("br_logger")
        self.logger.setLevel(logging.INFO)

    def navigate(self):
        column_list = [[col1_xpath, self.columns[0]],
                       [col2_xpath, self.columns[1]],
                       [col3_xpath, self.columns[2]]]

        try:
            self.driver.load_page(f'{self.columns[0]} Navigation')
            for items in column_list:
                self.selector(items[0], items[1])
        except Exception as err:
            if self.driver.element_locator(home_xpath):
                pass
            else:
                self.logger.error('Navigation Page not found.')
                raise

    def selector(self, xpath, name_column):
        self.driver.column_element_finder(xpath, name_column)
        self.driver.btn_click(nav_submit_btn_xpath)
