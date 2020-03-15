#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

import time
from multiprocessing import Process
from threading import Thread

import logger
from config import STANDBY_MINUTES as COUNTDOWN, LED_BRIGHTNESS, standby
from functions import clear

NAME = "countdown"
LOG = logger.get_logger(NAME)
EXPIRED = "Runtime expired"
STOPPED = "Stop requested, stopped"
threads = []


class CountdownThread(Thread):
    def __init__(self, function, stripe, name=None, n=COUNTDOWN):
        super(CountdownThread, self).__init__()
        self.n = n * 60
        self.do_run = True
        self._function = function
        self._strip = stripe
        if name is None:
            self._name = function
        else:
            self._name = name

    def _process(self):
        LOG.info(
            "Thread '{0}' initialized, start process '{1}' for {2} seconds".format(
                str(self._name), self._function, str(self.n)))
        func_p = Process(target=self._function, name=self._name, args=(self._strip,))
        func_p.start()
        return func_p

    def run(self):
        p = self._process()
        threads.append(self)
        while self.__getattribute__('do_run') and self.n > 0:
            self.n -= 1
            time.sleep(1)
        if self.n <= 0:
            from bot import external_request
            LOG.info("{0}: {1}".format(EXPIRED, str(self._function)))
            external_request(standby)
        p.terminate()
        clear(self._strip)
        self._strip.setBrightness(LED_BRIGHTNESS)
        threads.remove(self)

    def stop(self):
        self.do_run = False
        LOG.info("{0}: {1}".format(STOPPED, str(self._function)))

    @property
    def is_running(self) -> bool:
        return self.do_run


if __name__ == '__main__':
    pass
