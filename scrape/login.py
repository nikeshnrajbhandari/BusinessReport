"""Login handler."""

import logging
import pyotp

from base_class import Driver, DriverInit
from configs import *
from helpers.utils import decrypt_token


class Login(Driver):

    def __init__(self, driver: DriverInit, email, creds, otp, marketplace):
        super().__init__(driver)
        self.email = email
        self.creds = creds
        self.otp = otp
        self.marketplace = marketplace
        self.logger = logging.getLogger("br_logger")
        self.logger.setLevel(logging.INFO)

    def sign_in(self):
        self.send_key(email_xpath, self.email)
        self.send_key(pass_xpath, decrypt_token(self.creds))
        self.btn_click(signin_btn_xpath)

    def authentication(self):
        for param in self.otp:
            otp = pyotp.parse_uri(decrypt_token(param))
            try:
                self.load_page(f'{self.email} Authentication')
                self.send_key(auth_xpath, otp.now())
                self.btn_click(auth_btn_xpath)
                if self.element_locator(nav_header_xpath) is True:
                    break
            except Exception:
                continue

    def asc_login(self):
        if self.marketplace in {'ATVPDKIKX0DER', 'A2EUQ1WTGCTBG2', 'A1AM78C64UM0Y8'}:
            url = na_url
        else:
            url = eu_url
        self.load_page('Login Page', url, LOAD_WAIT)
        self.sign_in()
        self.authentication()
