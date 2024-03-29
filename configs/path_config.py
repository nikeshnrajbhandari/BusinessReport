"""XPath and key URL"""

# Browser URL
na_url = "https://sellercentral.amazon.com/signin?ref_=scus_soa_wp_signin_n"
eu_url = "https://sellercentral.amazon.co.uk/signin?ref_=scuk_soa_wp_signin_n"
na_br = "https://sellercentral.amazon.com/business-reports/ref=xx_sitemetric_dnav_xx"
eu_br = "https://sellercentral.amazon.co.uk/business-reports/ref=xx_sitemetric_dnav_xx#/dashboard"
na_sku = "https://sellercentral.amazon.com/business-reports#/report?id=102%3ADetailSalesTrafficBySKU&chartCols=&columns=&fromDate={s_date}&toDate={e_date}"
eu_sku = "https://sellercentral.amazon.co.uk/business-reports/ref=xx_sitemetric_dnav_xx#/report?id=102%3ADetailSalesTrafficBySKU&chartCols=&columns=0%2F1%2F3&fromDate={s_date}&toDate={e_date}"
na_asin = "https://sellercentral.amazon.com/business-reports#/report?id=102%3ADetailSalesTrafficByChildItem&chartCols=&columns=&fromDate={s_date}&toDate={e_date}"
eu_asin = "https://sellercentral.amazon.co.uk/business-reports/ref=xx_sitemetric_dnav_xx#/report?id=102%3ADetailSalesTrafficByChildItem&chartCols=&columns=0%2F1%2F3%2F4%2F6%2F8%2F10%2F12%2F14%2F16%2F18%2F20%2F22%2F24%2F26%2F28%2F30%2F32%2F34%2F36&fromDate={s_date}&toDate={e_date}"

# Login Page
email_xpath = '//*[@id="ap_email"]'
pass_xpath = '//*[@id="ap_password"]'
signin_btn_xpath = '//*[@id="signInSubmit"]'

# Authentication Page
auth_xpath = '//*[@id="auth-mfa-otpcode"]'
auth_btn_xpath = '//*[@id="auth-signin-button"]'
error_xpath = '//*[@id="auth-error-message-box"]/div/h4'

# Navigation Page
nav_tbl_xpath = '/html/body/div/div[2]/div[1]/div/div/div[1]/kat-box/div/div[3]/div/div[1]/div/div'
nav_header_xpath = '/html/body/div/div[2]/div[1]/div/div/div[1]/kat-box/h1'
col1_xpath = '//*[@id="picker-container"]/div/div[2]/div/div[1]/div/div/button/div/div[1]'
col2_xpath = '//*[@id="picker-container"]/div/div[2]/div/div[2]/div/div/button/div/div[1]'
col3_xpath = '//*[@id="picker-container"]/div/div[2]/div/div[3]/div/div/button/div/div[1]'
nav_submit_btn_xpath = '//*[@id="picker-container"]/div/div[3]/div/button'

# Download
home_xpath = '//*[@id="navbar"]/div[1]/a'
dashboard_xpath = '//*[@id="root"]/div/div[2]/div/div[2]/div[1]/h1'
na_download = '//*[@label="Download (.csv)"]'
eu_download = '//*[@label="Download CSV"]'
na_column_toggle = '//*[@label="SHOW/HIDE COLUMNS"]'
na_parent = '//*[@label="(Parent) ASIN"]'
