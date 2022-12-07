from os.path import dirname, abspath, join

BASE_DIR = dirname(dirname(abspath(__file__)))
FILE_DIR = join(BASE_DIR,'BusinessReport')
STAGE_DIR = join(FILE_DIR,'STAGE')
SKU_PRE_DIR = join(FILE_DIR,'SKU_PRE')
SKU_RAW_DIR = join(FILE_DIR,'SKU_RAW')
ASIN_STAGE_DIR = join(FILE_DIR,'ASIN_STAGE')
ASIN_PRE_DIR = join(FILE_DIR,'ASIN_PRE')
ASIN_RAW_DIR = join(FILE_DIR,'ASIN_RAW')


