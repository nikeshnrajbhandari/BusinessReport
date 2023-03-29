# XPath and key URL

# Browser URL
na_url = "https://sellercentral.amazon.com/signin?ref_=scus_soa_wp_signin_n&initialSessionID=143-2786064-8692101&ld=SCUSWPDirect"
eu_url = "https://sellercentral.amazon.co.uk/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fsellercentral.amazon.co.uk%2Fhome&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=sc_uk_amazon_v2&openid.mode=checkid_setup&language=en_GB&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=sc_uk_amazon_v2&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&ssoResponse=eyJ6aXAiOiJERUYiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiQTI1NktXIn0.W80OM3JSzY7BSVghTN_DvUL93t0-Vj-R7kR52R3QzrnOZaa0INhR9w.IMX_-x6G8DOEw2-m.M1eGT8QMHUXnKsuDtg8STgb4tv5Ih8eIJCpe_eFwC83vWnlcSTth3faedBDR_uxmehPNtG3b6yEWzz7W3r19pNSvco4yaxftj37PCvgkmkFWfqxfnuVAlezpjUy2zYyW11ZIOLEyAGmb7MXY4NI78-ChUlJr3p45nTs7UPpFzC_-oqPfL0mpSefNYi4A1AAUv_i5pnVe_mCXQehitr9jtzZ-FHWP4DafqWOMYBy4squPRblszjrOIJWyH-T8ZpxvvA.euKoijOu4PlT7jzxnUqfhQ"
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
