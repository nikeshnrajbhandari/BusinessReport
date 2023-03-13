import time

from config import auth_xpath, auth_btn_xpath
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager


class Driver:
    def __init__(self, headless=False):
        options = Options()
        headless = headless
        prefs = {
            'download.default_directory': 'BusinessReport/STAGE',
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False
        }
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service(executable_path='C:/Driver/chromedriver')
        # service = Service(executable_path=ChromeDriverManager().install())
        self._driver = webdriver.Chrome(service=service, options=options)
        self._driver.maximize_window()

    def element_locator(self, wait_param, wait_by=By.XPATH, wait_time=60):
        try:
            WebDriverWait(self._driver, wait_time).until(
                EC.visibility_of_element_located((wait_by, wait_param))
            )
            return True
        except TimeoutException:
            print("Element not found.")
            return False

    def load_page(self, page, url='', wait_time=60):
        if url != '':
            self._driver.get(url)
        try:
            WebDriverWait(self._driver, wait_time).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            print(f"{page} page loaded")
        except TimeoutException:
            print(f"{page} Loading taking too much time")
            raise

    def send_key(self, wait_param, key, wait_by=By.XPATH, wait_time=60):
        try:
            WebDriverWait(self._driver, wait_time).until(
                EC.visibility_of_element_located((wait_by, wait_param))
            )
            self._driver.find_element(wait_by, wait_param).send_keys(key)
        except TimeoutException:
            print("Field not found.")
            raise

    def btn_click(self, wait_param, wait_by=By.XPATH, wait_time=60):
        try:
            WebDriverWait(self._driver, wait_time).until(
                EC.visibility_of_element_located((wait_by, wait_param))
            )
            self._driver.find_element(wait_by, wait_param).click()
        except TimeoutException:
            print("Button not found.")
            raise

    def scroll_into_view(self, element):
        element.location_once_scrolled_into_view

    def column_element_finder(self, wait_param, name_column, wait_by=By.XPATH, wait_time=60):
        try:
            WebDriverWait(self._driver, wait_time).until(
                EC.visibility_of_element_located((wait_by, wait_param))
            )
            elements = self._driver.find_elements(wait_by, wait_param)
            for item in elements:
                item.location_once_scrolled_into_view
                if item.text == name_column:
                    item.click()
        except TimeoutException:
            print("Field not found.")
            raise

    def sku_download(self):
        pass

    def asin_download(self):
        pass

    def close_driver(self):
        self._driver.close()
        self._driver.quit()
