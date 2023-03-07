from helpers import make_dir, del_residue_files, client_list, credentail
import pandas as pd
from base_class import Driver
from scrape import Scrape


def client_func(row):
    if row['fraction'] == 0:
        Scrape.scrape_whole(Driver,row)
    elif row['fraction'] == 1:
        Scrape.scrape_fraction(Driver,row)            



def main():
    make_dir()
    del_residue_files()
    #pd.set_option('display.max_columns', None)
    client = client_list()
    client.apply(client_func, axis=1)
    
    
if __name__ == '__main__':
    main()