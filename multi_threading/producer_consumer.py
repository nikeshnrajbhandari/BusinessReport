
from scrape.download_module import DownloadModule
from threading import Barrier
from queue import Queue, Empty

import logging, time

class ProducerConsumer:
    def __init__(self, n_process):
        self.logger = logging.getLogger("br_logger")
        self.logger.setLevel(logging.INFO)
        self.queue = Queue()
        self.barrier = Barrier(n_process)
        self.failed_list = []
        self.put_condition = True

    def producer(self, clients, identifier):
        self.logger.info(f'Producer {identifier}: Running')
        if len(clients) != 0:
            for client in clients:
                self.queue.put(client)
                self.put_condition = False
        self.barrier.wait()
        self.queue.put(None)
        self.logger.info(f'Producer {identifier}: Done')

    def consumer(self, dates, download_dir, driver_dir, identifier):
        self.logger.info(f'Consumer {identifier}: Running')
        while True:
            try:
                item = self.queue.get(block=False)
            except Empty:
                self.logger.info(f'Consumer {identifier}: Waiting a while')
                time.sleep(5)
                continue

            # Checks if there shared buffer is empty, and closes the queue if None.
            if item is None:
                self.queue.put(item)
                break
            self.logger.info(f'Consumer {identifier} got :{item}')
            try:
                a = 1/0
                DownloadModule().br_download(item, dates, download_dir, driver_dir)
            except Exception as err:
                self.logger.exception(err)
                self.failed_list.append(item)
        self.logger.info(f'Consumer {identifier}: Done')
        return self.failed_list



