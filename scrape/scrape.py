from base_class import Driver

class Scrape(Driver):
    def __init__(self):
        self._header = True
        
    def scrape_whole(self,row):
        print('Whole')
        print(row)
    
    def scrape_fraction(self,row):
        print('Whole')
        print(row)