from os.path import dirname, abspath, join

BASE_DIR = dirname(dirname(abspath(__file__)))
FILE_DIR = join(BASE_DIR, 'BusinessReport')
STAGE_DIR = join(FILE_DIR, 'STAGE')
SKU_PRE_DIR = join(FILE_DIR, 'SKU_PRE')
SKU_RAW_DIR = join(FILE_DIR, 'SKU_RAW')
ASIN_STAGE_DIR = join(FILE_DIR, 'ASIN_STAGE')
ASIN_PRE_DIR = join(FILE_DIR, 'ASIN_PRE')
ASIN_RAW_DIR = join(FILE_DIR, 'ASIN_RAW')
config_files = join(BASE_DIR, 'config_file')

PULL_TYPE = 'WEEKLY'
# PULL_TYPE = 'Monthly'
LOAD_WAIT = 60

SKU_HEADER = ['(Parent) ASIN', '(Child) ASIN', 'SKU']
WITHOUTASIN_HEADER = ['(Parent) ASIN', '(Child) ASIN', 'Title', 'Sessions - Mobile App', 'Sessions - Browser',
          'Sessions - Total', 'Session Percentage - Mobile App', 'Session Percentage - Browser',
          'Session Percentage - Total', 'Page Views - Mobile App', 'Page Views - Browser', 'Page Views - Total',
          'Page Views Percentage - Mobile App', 'Page Views Percentage - Browser', 'Page Views Percentage - Total',
          'Featured Offer (Buy Box) Percentage', 'Units Ordered', 'Unit Session Percentage', 'Ordered Product Sales',
          'Total Order Items']
