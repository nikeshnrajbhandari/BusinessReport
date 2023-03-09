import time

import pyotp
from config import auth_xpath, auth_btn_xpath
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager


class Selenium:
    def __init__(self, headless=False):
        options = Options()
        headless = headless
        prefs = {
            'download.default_directory': 'C:/Users/nnrajbhandari/Documents/Python/BR/BusinessReport/STAGE',
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

    def page_load_check(self, page, wait_time=60):
        try:
            WebDriverWait(self._driver, wait_time).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            print(f"{page} page loaded")
        except TimeoutException:
            print(f"{page} Loading taking too much time")
            raise

    def element_locator(self, wait_param, wait_by=By.XPATH, wait_time=60):
        try:
            WebDriverWait(self._driver, wait_time).until(
                EC.visibility_of_element_located((wait_by, wait_param))
            )
        except TimeoutException:
            print("Element not found.")
            raise

    def load_page(self, url, wait_time=60):
        self._driver.get(url)
        try:
            WebDriverWait(self._driver, wait_time).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            print("Page loaded")
        except TimeoutException:
            print("Loading taking too much time")
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

    def auth(self, auth_param):
        otp = pyotp.parse_uri(auth_param)
        Selenium.page_load_check(self,'Authentication')
        Selenium.send_key(self, auth_xpath, otp.now())
        Selenium.btn_click(self, auth_btn_xpath)


