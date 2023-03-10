# XPath and key URL

# Browser URL
na_url = "https://sellercentral.amazon.com/signin?ref_=scus_soa_wp_signin_n&initialSessionID=143-2786064-8692101&ld=SCUSWPDirect"
eu_url = "https://sellercentral.amazon.co.uk/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fsellercentral.amazon.co.uk%2Fhome&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=sc_uk_amazon_v2&openid.mode=checkid_setup&language=en_GB&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=sc_uk_amazon_v2&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&ssoResponse=eyJ6aXAiOiJERUYiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiQTI1NktXIn0.W80OM3JSzY7BSVghTN_DvUL93t0-Vj-R7kR52R3QzrnOZaa0INhR9w.IMX_-x6G8DOEw2-m.M1eGT8QMHUXnKsuDtg8STgb4tv5Ih8eIJCpe_eFwC83vWnlcSTth3faedBDR_uxmehPNtG3b6yEWzz7W3r19pNSvco4yaxftj37PCvgkmkFWfqxfnuVAlezpjUy2zYyW11ZIOLEyAGmb7MXY4NI78-ChUlJr3p45nTs7UPpFzC_-oqPfL0mpSefNYi4A1AAUv_i5pnVe_mCXQehitr9jtzZ-FHWP4DafqWOMYBy4squPRblszjrOIJWyH-T8ZpxvvA.euKoijOu4PlT7jzxnUqfhQ"
# Login Page
email_xpath = '//*[@id="ap_email"]'
pass_xpath = '//*[@id="ap_password"]'
signin_btn_xpath = '//*[@id="signInSubmit"]'

# Authentication Page
auth_xpath = '//*[@id="auth-mfa-otpcode"]'
auth_btn_xpath = '//*[@id="auth-signin-button"]'
error_xpath = '//*[@id="auth-error-message-box"]/div/h4'

# Navigation Page
nav_header_xpath = '/html/body/div/div[2]/div[1]/div/div/div[1]/kat-box/h1'
nav_xpath = '//*[@id="picker-container"]/div/div[2]/'
