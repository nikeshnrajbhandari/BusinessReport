"""Login handler."""

import logging
import pyotp

from base_class import Driver, DriverInit
from configs import *
from helpers.utils import decrypt_token


class Login(Driver):

    def __init__(self, driver: DriverInit, name, email, creds, otp, marketplace):
        super().__init__(driver)
        self.name = name
        self.email = email
        self.creds = creds
        self.otp = otp
        self.marketplace = marketplace
        self.logger = logging.getLogger("br_logger")
        self.logger.setLevel(logging.INFO)

    def sign_in(self):
        self.send_key(self.name, email_xpath, self.email)
        self.send_key(self.name, pass_xpath, decrypt_token(self.creds))
        self.btn_click(self.name, signin_btn_xpath)

    def authentication(self):
        for param in self.otp:
            otp = pyotp.parse_uri(decrypt_token(param))
            try:
                self.load_page(self.name, 'Authentication',wait_time=LOAD_WAIT)
                self.send_key(self.name, auth_xpath, otp.now(), wait_time=LOAD_WAIT)
                self.btn_click(self.name, auth_btn_xpath, wait_time=LOAD_WAIT)
                if self.element_locator(self.name, nav_header_xpath, wait_time=LOAD_WAIT) is True:
                    break
            except Exception:
                continue

    def asc_login(self):
        if self.marketplace in {'ATVPDKIKX0DER', 'A2EUQ1WTGCTBG2', 'A1AM78C64UM0Y8'}:
            url = na_url
        else:
            url = eu_url
        self.load_page(self.name, 'Login Page', url, wait_time=LOAD_WAIT)
        self.sign_in()
        self.authentication()
