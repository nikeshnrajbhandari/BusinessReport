from config import *
from helpers import date_range
class Scraper:
    def __init__(self, driver, seller_id, marketplace_id, name, wasin, fraction):
        self.driver = driver
        self.seller_id = seller_id
        self.marketplace_id = marketplace_id
        self.name = name
        self.wasin = wasin
        self.fraction = fraction


    def scrape(self):

        start_date, end_date = date_range(PULL_TYPE)
        if self.marketplace_id == 'ATVPDKIKX0DER':
            self.north_america(start_date,end_date)
        else:
            self.europe(start_date,end_date)



    def north_america(self,start_date,end_date):
        pass

    def europe(self,start_date,end_date):
        pass

