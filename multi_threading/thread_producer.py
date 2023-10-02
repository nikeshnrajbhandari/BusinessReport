from threading import Thread
from helpers.client_helper import client_helper
from scrape.download_module import DownloadModule
from threading import Barrier
from queue import Queue, Empty
import logging, time


class CustomThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return


class ThreadProducer:
    def __init__(self, n_process=4):
        self.n_process = n_process
        self.queue = Queue()
        self.barrier = Barrier(n_process)
        self.failed_list = []
        self.logger = logging.getLogger("br_logger")
        self.logger.setLevel(logging.INFO)

    def producer(self, clients, identifier):
        self.logger.info(f'Producer {identifier}: Running')
        if len(clients) != 0:
            for client in clients:
                self.queue.put(client)
        self.barrier.wait()
        self.queue.put(None)
        self.logger.info(f'Producer {identifier}: Done')

    def consumer(self, dates, download_dir, driver_dir, identifier):
        self.logger.info(f'Consumer {identifier}: Running')
        while True:
            try:
                item = self.queue.get()
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
                DownloadModule().br_download(item, dates, download_dir, driver_dir)
            except Exception as err:
                self.logger.exception(err)
                self.failed_list.append(item)
        self.logger.info(f'Consumer {identifier}: Done')

    def task_producer(self, client_list, dates, part_dir, count=0):
        # print(client_list)
        consumers = [CustomThread(target=self.consumer, args=(dates, part[0], part[1], part[2])) for part in
                     part_dir]

        producers = [CustomThread(target=self.producer, args=(chunks[0], chunks[1])) for chunks in
                     client_list]

        for threads in consumers:
            threads.start()

        for threads in producers:
            threads.start()

        for threads in producers:
            threads.join()

        for threads in consumers:
            threads.join()

        if len(self.failed_list) > 0 and count < 3:
            time.sleep(60)

            self.logger.info('Retrying for:')
            for item in self.failed_list:
                self.logger.info(item)

            del producers, consumers, self.queue, self.barrier

            task = ThreadProducer(self.n_process)
            task.task_producer(client_list=client_helper(self.failed_list), dates=dates, part_dir=part_dir, count=count + 1)
