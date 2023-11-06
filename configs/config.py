"""Project level configurations"""

from file_helper.custom_helper import project_dir, download_dir,stage_dir, driver_dir, log_dir, join_dir

"""Thread Config"""
n_process = 4

"""Folder Config"""
project_dir = project_dir()
download_dir = download_dir()
stage_dir = stage_dir()
driver_dir = driver_dir()
log_dir = log_dir()
sku_pre_dir = join_dir(download_dir, 'SKU_PRE')
sku_raw_dir = join_dir(download_dir, 'SKU_RAW')
asin_pre_dir = join_dir(download_dir, 'ASIN_PRE')
asin_raw_dir = join_dir(download_dir, 'ASIN_RAW')
config_files = join_dir(join_dir(project_dir,'BR'), 'config_file')
# client_file = join_dir(config_files, 'All_clients - Copy.csv')
client_file = join_dir(config_files, 'All_clients.csv')
cred_file = join_dir(config_files, 'Credentials.csv')
auth_file = join_dir(config_files, 'Authentication.csv')

"""Selenium Config"""

headless = False
LOAD_WAIT = 120
SKU_HEADER = ['(Parent) ASIN', '(Child) ASIN', 'SKU']
WITHOUTASIN_HEADER = ['(Parent) ASIN', '(Child) ASIN', 'Title', 'Sessions - Mobile App', 'Sessions - Browser',
                      'Sessions - Total', 'Session Percentage - Mobile App', 'Session Percentage - Browser',
                      'Session Percentage - Total', 'Page Views - Mobile App', 'Page Views - Browser',
                      'Page Views - Total',
                      'Page Views Percentage - Mobile App', 'Page Views Percentage - Browser',
                      'Page Views Percentage - Total',
                      'Featured Offer (Buy Box) Percentage', 'Units Ordered', 'Unit Session Percentage',
                      'Ordered Product Sales',
                      'Total Order Items']
