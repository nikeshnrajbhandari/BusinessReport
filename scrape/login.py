import pyotp
import logging

from config import *
from helpers.utils import decrypt_token


class Login:

    def __init__(self, driver, email, creds, otp, marketplace):
        self.driver = driver
        self.email = email
        self.creds = creds
        self.otp = otp
        self.marketplace = marketplace
        self.logger = logging.getLogger("br_logger")
        self.logger.setLevel(logging.INFO)

    def sign_in(self):
        self.driver.send_key(email_xpath, self.email)
        self.driver.send_key(pass_xpath, decrypt_token(self.creds))
        self.driver.btn_click(signin_btn_xpath)

    def authentication(self):
        for param in self.otp:
            otp = pyotp.parse_uri(decrypt_token(param))
            try:
                self.driver.load_page('Authentication')
                self.driver.send_key(auth_xpath, otp.now())
                self.driver.btn_click(auth_btn_xpath)
                if self.driver.element_locator(nav_header_xpath) is True:
                    break
            except Exception:
                continue

    def asc_login(self):
        if self.marketplace in {'ATVPDKIKX0DER', 'A2EUQ1WTGCTBG2', 'A1AM78C64UM0Y8'}:
            url = na_url
        else:
            url = eu_url
        self.driver.load_page('Login Page', url, LOAD_WAIT)
        self.sign_in()
        self.authentication()
