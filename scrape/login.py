from base_class import Selenium
from config import *
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class Login(Selenium):
    def __init__(self, email, creds, otp):
        self.email = email
        self.creds = creds
        self.otp = otp
        super().__init__()

    def sign_in(self):
        self.send_key(email_xpath, self.email)
        self.send_key(pass_xpath, self.creds)
        self.btn_click(signin_btn_xpath)

    def authentication(self):
        for param in self.otp:
            self.auth(param)

    def asc_login(self):
        url = na_url
        self.load_page(url, LOAD_WAIT)
        Login.sign_in(self)
        Login.authentication(self)
