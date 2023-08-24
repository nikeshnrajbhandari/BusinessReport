from os import makedirs

from file_helper.custom_helper import stage_dir, driver_dir, join_dir

class CustomDir:
    def __init__(self, n_process = 4):
        self.download_list = list()
        self.driver_list = list()
        self.id_list = list()
        self.n_process = n_process

    def dir_init(self):
        for i in range(1, self.n_process+1):
            download_path = join_dir(stage_dir(),f's{i}')
            makedirs(download_path, exist_ok=True)
            self.download_list.append(download_path)

            driver_path = join_dir(driver_dir(), f's{i}')
            makedirs(driver_path, exist_ok=True)
            self.driver_list.append(driver_path)
            self.id_list.append(f's{i}')

    def folder_info(self):
        self.dir_init()
        return list(zip(self.download_list, self.driver_list, self.id_list))

# if __name__ == '__main__':
#     a = CustomDir(4)
#     print(a.folder_info())