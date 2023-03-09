from os.path import dirname, abspath, join

BASE_DIR = dirname(dirname(abspath(__file__)))
FILE_DIR = join(BASE_DIR,'BusinessReport')
STAGE_DIR = join(FILE_DIR,'STAGE')
SKU_PRE_DIR = join(FILE_DIR,'SKU_PRE')
SKU_RAW_DIR = join(FILE_DIR,'SKU_RAW')
ASIN_STAGE_DIR = join(FILE_DIR,'ASIN_STAGE')
ASIN_PRE_DIR = join(FILE_DIR,'ASIN_PRE')
ASIN_RAW_DIR = join(FILE_DIR,'ASIN_RAW')
config_files = join(BASE_DIR, 'config_file')

PULL_TYPE = 'Weekly'
# PULL_TYPE = 'Monthly'
LOAD_WAIT = 60

na_url = "https://sellercentral.amazon.com/signin?ref_=scus_soa_wp_signin_n&initialSessionID=143-2786064-8692101&ld=SCUSWPDirect"
email_xpath = '//*[@id="ap_email"]'
pass_xpath = '//*[@id="ap_password"]'
signin_btn_xpath = '//*[@id="signInSubmit"]'

auth_xpath = '//*[@id="auth-mfa-otpcode"]'
auth_btn_xpath = '//*[@id="auth-signin-button"]'

