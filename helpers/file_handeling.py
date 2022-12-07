from config import FILE_DIR, STAGE_DIR, SKU_PRE_DIR, SKU_RAW_DIR, ASIN_PRE_DIR, ASIN_RAW_DIR 

import os

def make_dir():
    dir_list = [
        FILE_DIR, STAGE_DIR, SKU_PRE_DIR, SKU_RAW_DIR, ASIN_PRE_DIR, ASIN_RAW_DIR 
    ]
    
    for dir in dir_list:
        os.makedirs(dir, exist_ok=True)
        
def del_residue_files():
    for each_dir in [SKU_PRE_DIR, ASIN_PRE_DIR]:
        for each_file in os.listdir(each_dir):
            os.remove(os.path.join(each_dir, each_file))