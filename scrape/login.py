from config import *
import pyotp


class Login:
    def __init__(self, driver, email, creds, otp, marketplace):
        self.driver = driver
        self.email = email
        self.creds = creds
        self.otp = otp
        self.marketplace = marketplace

    def sign_in(self):
        self.driver.send_key(email_xpath, self.email)
        self.driver.send_key(pass_xpath, self.creds)
        self.driver.btn_click(signin_btn_xpath)

    def authentication(self):
        for param in self.otp:
            otp = pyotp.parse_uri(param)
            try:
                self.driver.load_page('Authentication')
                self.driver.send_key(auth_xpath, otp.now())
                self.driver.btn_click(auth_btn_xpath)
                if self.driver.element_locator(nav_header_xpath) is True:
                    break
            except Exception:
                continue

    def asc_login(self):
        if self.marketplace == 'ATVPDKIKX0DER':
            url = na_url
        else:
            url = eu_url
        self.driver.load_page('Login Page', url, LOAD_WAIT)
        self.sign_in()
        self.authentication()
