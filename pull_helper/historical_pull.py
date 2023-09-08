from scrape.download_module import DownloadModule

import logging, time


class HistoricalPull:
    def __init__(self, client_id, dates, part_dir):
        self.logger = logging.getLogger("br_logger")
        self.logger.setLevel(logging.INFO)
        self.client_id = client_id
        self.dates = dates
        self.part_dir = part_dir

    def pull_helper(self):
        # pull_list = list(zip(self.client_id, self.dates, self.part_dir[0][0], self.part_dir[0][1]))
        pull_list = [[self.client_id, item, self.part_dir[0][0], self.part_dir[0][1]] for item in self.dates]
        self.historical_pull(pull_list)

    def historical_pull(self, pull_list, count=0):
        failed_list = []
        for item in pull_list:
            # print(item)
            try:
                DownloadModule().br_download(item[0], item[1], item[2], item[3])
            except Exception as err:
                self.logger.exception(err)
                failed_list.append(item)

        if len(failed_list) > 0 and count < 3:
            time.sleep(100)
            self.logger.info('Retrying for:')
            for item in failed_list:
                self.logger.info(item)
            self.historical_pull(failed_list, count=count + 1)
