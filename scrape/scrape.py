from base_class import Selenium

class Scrape(Selenium):
    def __init__(self):
        self._header = True
        
    def scrape_whole(self,row):
        print('Whole')
        print(row)
    
    def scrape_fraction(self,row):
        print('Whole')
        print(row)