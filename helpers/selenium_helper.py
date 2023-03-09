# def auth_init(otp):
#     otp = pyotp.parse_uri(otp)
#     driver.find_element(By.XPATH, '//*[@id="auth-mfa-otpcode"]').send_keys(otp.now())
#     driver.find_element(By.XPATH, '//*[@id="auth-signin-button"]').click()
#
#
# def marketplace_nav(co1, co2, co3):
#     first = False
#     i = 1
#     while first == False:
#         try:
#             WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
#                 (By.XPATH, f'//*[@id="picker-container"]/div/div[2]/div/div[1]/div/div[{i}]/button/div/div')))
#             seller = driver.find_element(By.XPATH,
#                                          f'//*[@id="picker-container"]/div/div[2]/div/div[1]/div/div[{i}]/button/div/div[1]').text
#             if seller == co1:
#                 driver.find_element(By.XPATH,
#                                     f'//*[@id="picker-container"]/div/div[2]/div/div[1]/div/div[{i}]/button').click()
#                 first = True
#                 second = False
#                 j = 1
#                 while second == False:
#                     try:
#                         WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,
#                                                                                          f'//*[@id="picker-container"]/div/div[2]/div/div[2]/div/div[{j}]/button/div/div')))
#                         seller_name = driver.find_element(By.XPATH,
#                                                           f'//*[@id="picker-container"]/div/div[2]/div/div[2]/div/div[{j}]/button/div/div[1]').text
#                         if seller_name == co2:
#                             driver.find_element(By.XPATH,
#                                                 f'//*[@id="picker-container"]/div/div[2]/div/div[2]/div/div[{j}]/button').click()
#                             second = True
#                             third = False
#                             k = 1
#                             while third == False:
#                                 try:
#                                     WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,
#                                                                                                      f'//*[@id="picker-container"]/div/div[2]/div/div[3]/div/div[{k}]/button/div/div')))
#                                     liElement = driver.find_element(By.XPATH,
#                                                                     f'//*[@id="picker-container"]/div/div[2]/div/div[3]/div/div[{k}]/button/div/div')
#                                     driver.execute_script("arguments[0].scrollIntoView(true);", liElement)
#                                     region = driver.find_element(By.XPATH,
#                                                                  f'//*[@id="picker-container"]/div/div[2]/div/div[3]/div/div[{k}]/button/div/div[1]').text
#                                     if region == co3:
#                                         driver.find_element(By.XPATH,
#                                                             f'//*[@id="picker-container"]/div/div[2]/div/div[3]/div/div[{k}]/button').click()
#                                         driver.find_element(By.XPATH,
#                                                             '//*[@id="picker-container"]/div/div[3]/div/button').click()
#                                         third = True
#                                     k = k + 1
#                                 except TimeoutException:
#                                     print('Time out')
#                                     driver.refresh()
#                                 except NoSuchElementException:
#                                     print('Server error')
#                                     break
#                         j = j + 1
#                     except TimeoutException:
#                         print('Time out')
#                         driver.refresh()
#                     except NoSuchElementException:
#                         print('Server error')
#                         break
#             i = i + 1
#         except TimeoutException:
#             print('Time out')
#             driver.refresh()
#         except NoSuchElementException:
#             print('Server error')
#             break
#
#
# def sku(s_date, e_date):
#     driver.get("https://sellercentral.amazon.com/business-reports/ref=xx_sitemetric_dnav_xx")
#     driver.get(
#         f"https://sellercentral.amazon.com/business-reports/ref=xx_sitemetric_dnav_xx#/report?id=102%3ADetailSalesTrafficBySKU&chartCols=&columns=0%2F1%2F3&fromDate={s_date}&toDate={e_date}")
#     driver.refresh()
#     # driver.get("https://sellercentral.amazon.com/business-reports/ref=xx_sitemetric_dnav_xx#/report?id=102%3ADetailSalesTrafficBySKU&chartCols=&columns=0%2F1%2F3&fromDate=2022-08-14&toDate=2022-08-20")
#
#
# def withouASIN(s_date, e_date, buyer):
#     driver.get("https://sellercentral.amazon.com/business-reports/ref=xx_sitemetric_dnav_xx")
#     if buyer == 'B2B':
#         # driver.get(f"https://sellercentral.amazon.com/business-reports/ref=xx_sitemetric_dnav_xx#/report?id=102%3ADetailSalesTrafficByChildItem&chartCols=&columns=0%2F1%2F3%2F4%2F5%2F6%2F7%2F8%2F9%2F10%2F11%2F12%2F13%2F14%2F15%2F16%2F17%2F19%2F21%2F23&fromDate={s_date}&toDate={e_date}")
#         driver.get(
#             f"https://sellercentral.amazon.com/business-reports/ref=xx_sitemetric_dnav_xx#/report?id=102%3ADetailSalesTrafficByChildItem&chartCols=&columns=0%2F1%2F3%2F4%2F6%2F8%2F10%2F12%2F14%2F16%2F18%2F20%2F22%2F24%2F26%2F28%2F30%2F32%2F34%2F36&fromDate={s_date}&toDate={e_date}")
#
#         driver.refresh()
#     elif buyer == 'NOB2B':
#         driver.get(
#             f"https://sellercentral.amazon.com/business-reports/ref=xx_sitemetric_dnav_xx#/report?id=102%3ADetailSalesTrafficByChildItem&chartCols=&columns=0%2F1%2F3%2F4%2F5%2F6%2F7%2F8%2F9%2F10%2F11%2F12%2F13%2F14%2F15%2F16%2F17%2F18%2F19%2F20&fromDate={s_date}&toDate={e_date}")
#         driver.refresh()
#         # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
#         # time.sleep(3)
#         # driver.save_screenshot(name+'.png')
#
#
# def download():
#     try:
#         WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@label="Download (.csv)"]')))
#         driver.find_element(By.XPATH, '//*[@label="Download (.csv)"]').click()
#     except TimeoutException:
#         print('Couldnt find download button.')