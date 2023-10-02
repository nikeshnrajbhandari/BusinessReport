
from scrape.download_module import DownloadModule
from threading import Barrier
from queue import Queue, Empty

import logging, time

class ProducerConsumer:
    def __init__(self, n_process):
        self.logger = logging.getLogger("br_logger")
        self.logger.setLevel(logging.INFO)






