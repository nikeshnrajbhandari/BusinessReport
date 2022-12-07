
from selenium import webdriver

from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager
# def get_driver():
#     options = Options()
#     options.headless = False
#     prefs = {
#         'download.default_directory': 'C:/Users/nnrajbhandari/Documents/Python/BR/BusinessReport/STAGE',
#         "download.prompt_for_download": False,
#         "download.directory_upgrade": True,
#         "safebrowsing_for_trusted_sources_enabled": False,
#         "safebrowsing.enabled": False
#         }
#     options.add_experimental_option("prefs",prefs)
#     options.add_experimental_option('excludeSwitches', ['enable-logging'])
#     service = Service(executable_path='C:/Driver/chromedriver')
#     # service = Service(executable_path=ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=options)
#     return driver

# def page_load(driver):
#     print('Load Page')

class Driver:
    def __init__(self, url='', headless=False):
        self.__url = url
        options = Options()
        headless = headless
        prefs = {
            'download.default_directory': 'C:/Users/nnrajbhandari/Documents/Python/BR/BusinessReport/STAGE',
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False
            }
        options.add_experimental_option("prefs",prefs)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service(executable_path='C:/Driver/chromedriver')
        # service = Service(executable_path=ChromeDriverManager().install())
        self._driver = webdriver.Chrome(service=service, options=options)
        self._driver.maximize_window()
        
    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
            self._url = url
    
    def load_page(self, wait_time=60):
        self._driver.get(self._url)
        try:
            WebDriverWait(self._driver, wait_time).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            print("Page Loaded")
        except TimeoutException:
            print("loading taking too much time")
            raise
        
    def __del__(self):
        # commented for testing
        try:
            self._driver.close()
        except Exception:
            print("unable to close driver")
        # pass