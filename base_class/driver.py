import logging

from config import *
from selenium import webdriver
from contextlib import contextmanager
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager


class Driver:

    def __init__(self, headless=False):
        options = ChromeOptions()
        prefs = {
            'download.default_directory': STAGE_DIR,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False
        }
        if headless:
            options.add_argument("--headless=new")

        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service(executable_path='C:/Driver/chromedriver')
        # service = Service(executable_path=ChromeDriverManager().install())
        self._driver = webdriver.Chrome(service=service, options=options)
        self._driver.maximize_window()
        self.logger = logging.getLogger("br_logger")
        self.logger.setLevel(logging.INFO)

    def element_locator(self, wait_param, wait_by=By.XPATH, wait_time=60):
        try:
            WebDriverWait(self._driver, wait_time).until(
                EC.visibility_of_element_located((wait_by, wait_param))
            )
            return True
        except TimeoutException:
            self.logger.exception("Element not found.")
            return False

    def load_page(self, page, url='', wait_time=60):
        if url != '':
            self._driver.get(url)
        try:
            WebDriverWait(self._driver, wait_time).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            self.logger.info(f"{page} page loaded")
        except TimeoutException:
            self.logger.exception(f"{page} Loading taking too much time")
            raise

    def send_key(self, wait_param, key, wait_by=By.XPATH, wait_time=60):
        try:
            WebDriverWait(self._driver, wait_time).until(
                EC.visibility_of_element_located((wait_by, wait_param))
            )
            self._driver.find_element(wait_by, wait_param).send_keys(key)
        except TimeoutException:
            self.logger.exception("Field not found.")
            raise

    def btn_click(self, wait_param, wait_by=By.XPATH, wait_time=60):
        try:
            WebDriverWait(self._driver, wait_time).until(
                EC.visibility_of_element_located((wait_by, wait_param))
            )
            self._driver.find_element(wait_by, wait_param).click()
        except TimeoutException:
            self.logger.exception("Button not found.")
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
            self.logger.exception("Field not found.")
            raise

    def every_downloads_chrome(self):
        if not self._driver.current_url.startswith("chrome://downloads"):
            self._driver.get("chrome://downloads/")
        while True:
            path = self._driver.execute_script("""
                var items = document.querySelector('downloads-manager')
                    .shadowRoot.getElementById('downloadsList').items;
                if (items.every(e => e.state === "COMPLETE"))
                    return items.map(e => e.fileUrl || e.file_url);
                """)
            if path:
                break
        return True

    @contextmanager
    def wait_for_new_window(self, handles, wait_time=60):
        WebDriverWait(self._driver, wait_time).until(
            lambda driver: len(handles) != len(driver.window_handles))
        WebDriverWait(self._driver, wait_time).until(
            lambda driver: len(handles) == len(driver.window_handles))

    def expand_shadow_element(self, element):
        shadow_root = self._driver.execute_script('return arguments[0].shadowRoot', element)
        return shadow_root

    def rm_downloaded_item(self):
        root1 = self._driver.find_element(By.TAG_NAME, 'downloads-manager')
        shadow_root1 = self.expand_shadow_element(root1)

        root2 = shadow_root1.find_element(By.CSS_SELECTOR, '#frb0')
        shadow_root2 = self.expand_shadow_element(root2)
        try:
            WebDriverWait(shadow_root2, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#remove')))
        except TimeoutException:
            self.logger.exception("Couldn't find element")
        root3 = shadow_root2.find_element(By.CSS_SELECTOR, '#remove')
        shadow_root3 = self.expand_shadow_element(root3)
        close_button = shadow_root3.find_element(By.CSS_SELECTOR, '#maskedImage')
        close_button.click()

    def close_driver(self):
        self._driver.close()
        self._driver.quit()
