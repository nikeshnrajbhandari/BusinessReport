class Navigation:
    def __init__(self, driver, col1, col2, col3):
        self.driver = driver
        self.columns = [col1, col2, col3]

    def navigate(self):
        print(self.columns)
        # self.driver.load_page('Navigation')
        # for items in self.columns:
        #     print(items)

    def selector(self):
        pass
