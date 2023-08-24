from threading import Thread
from multi_threading.producer_consumer import ProducerConsumer
from helpers.client_helper import client_helper

import time
import logging

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


class ThreadProducer(ProducerConsumer):
    def __init__(self, n_process=4):
        super().__init__(n_process)
        self.logger = logging.getLogger("br_logger")
        self.logger.setLevel(logging.INFO)

    def task_producer(self, client_list, dates, part_dir, count=0, failed_list=[]):
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
            # failed_list = threads.join()
            failed_list= (threads.join())

        if len(failed_list) > 0 and count < 3:
            time.sleep(20)
            del producers, consumers, self.queue
            self.logger.info('Retrying for:')
            for item in failed_list:
                self.logger.info(item)

            self.task_producer(client_helper(failed_list), dates, part_dir, count + 1)
