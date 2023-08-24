from configs.config import n_process
from multi_threading.thread_producer import ThreadProducer


class RegularPull:
    def __init__(self, client_list, dates, part_dir):
        self.client_list = client_list
        self.dates = dates
        self.part_dir = part_dir


    def regular_pull(self):
        task = ThreadProducer(n_process)
        task.task_producer(client_list=self.client_list, dates=self.dates, part_dir=self.part_dir)
