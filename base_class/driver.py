""" Selenium browser class"""
import sys
import threading
import logging

from contextlib import contextmanager
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager


class DriverInit:
    def __init__(self, download_dir, driver_dir, headless=False):
        options = ChromeOptions()
        prefs = {
            'download.default_directory': download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False
        }
        if headless:
            options.add_argument("--headless=new")

        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # lock = threading.Lock()
        # lock.acquire()

        cache_manager = DriverCacheManager(root_dir=driver_dir)
        driver_path = ChromeDriverManager(cache_manager=cache_manager).install()
        # lock.release()

        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()

    def get_driver(self):
        return self.driver

    def __del__(self):
        try:
            self.driver.close()
            self.driver.quit()
        except Exception:
            sys.exit('Exiting due to exception in Driver exit operation!')


class Driver:
    def __init__(self, driver: DriverInit):
        self.driver_obj = driver
        self.driver = self.driver_obj.get_driver()
        self.logger = logging.getLogger("br_logger")
        self.logger.setLevel(logging.INFO)

    def element_locator(self, name, wait_param, wait_by=By.XPATH, wait_time=60):
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located((wait_by, wait_param))
            )
            return True
        except TimeoutException:
            self.logger.error(f"[{name}] Element not found.")
            return False

    def load_page(self, name, page, url='', wait_time=60):
        if url != '':
            self.driver.get(url)
        try:
            WebDriverWait(self.driver, wait_time).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            self.logger.info(f"[{name}] {page} page loaded")
        except TimeoutException:
            self.logger.error(f"[{name}] {page} Loading taking too much time")
            raise

    def send_key(self, name, wait_param, key, wait_by=By.XPATH, wait_time=60):
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located((wait_by, wait_param))
            )
            self.driver.find_element(wait_by, wait_param).send_keys(key)
        except TimeoutException:
            self.logger.error(f"[{name}] Field not found.")
            raise

    def btn_click(self, name, wait_param, wait_by=By.XPATH, wait_time=60):
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located((wait_by, wait_param))
            )
            self.driver.find_element(wait_by, wait_param).click()
        except TimeoutException:
            self.logger.error(f"[{name}] Button not found.")
            raise

    def scroll_into_view(self, element):
        element.location_once_scrolled_into_view

    def column_element_finder(self, name, wait_param, name_column, wait_by=By.XPATH, wait_time=60):
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located((wait_by, wait_param))
            )
            elements = self.driver.find_elements(wait_by, wait_param)
            for item in elements:
                self.scroll_into_view(item)
                if item.text == name_column:
                    item.click()
        except TimeoutException:
            self.logger.error(f"[{name}] Navigation column element not found.")
            raise

    # Checks Chrome download to verify the status of the download
    def every_downloads_chrome(self):
        if not self.driver.current_url.startswith("chrome://downloads"):
            self.driver.get("chrome://downloads/")
        while True:
            path = self.driver.execute_script("""
                return document.querySelector('downloads-manager')
                    .shadowRoot.getElementById('downloadsList').items;
                """)

                # ("""
                # var items = document.querySelector('downloads-manager')
                #     .shadowRoot.getElementById('downloadsList').items;
                # if (items.every(e => e.state === "COMPLETE"))
                #     return items.map(e => e.fileUrl || e.file_url);
                # """)
            # print(path[0]['state'])
            if path[0]['state'] == 2:
                break
        return True

    @contextmanager
    def wait_for_new_window(self, handles, wait_time=60):
        WebDriverWait(self.driver, wait_time).until(
            lambda driver: len(handles) != len(driver.window_handles))
        WebDriverWait(self.driver, wait_time).until(
            lambda driver: len(handles) == len(driver.window_handles))

    def expand_shadow_element(self, element):
        shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
        return shadow_root

    # Clears chorme download list
    def rm_downloaded_item(self, name):
        root1 = self.driver.find_element(By.TAG_NAME, 'downloads-manager')
        shadow_root1 = self.expand_shadow_element(root1)

        root2 = shadow_root1.find_element(By.CSS_SELECTOR, '#frb0')
        shadow_root2 = self.expand_shadow_element(root2)
        try:
            WebDriverWait(shadow_root2, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#remove')))
        except TimeoutException:
            self.logger.error(f"[{name}] Couldn't find element")
        root3 = shadow_root2.find_element(By.CSS_SELECTOR, '#remove')
        shadow_root3 = self.expand_shadow_element(root3)
        close_button = shadow_root3.find_element(By.CSS_SELECTOR, '#maskedImage')
        close_button.click()

    def wait_function(self, wait_param, wait_by=By.XPATH, wait_time=60):
        WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located((wait_by, wait_param))
        )
