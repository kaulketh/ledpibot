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


class CountdownThread(Thread):
    threads = []
    name = "Countdown"

    def __init__(self, function, stripe, name=None, n=COUNTDOWN):
        super(CountdownThread, self).__init__()
        self.expired = "Runtime expired"
        self.stopped = "Stop requested, stopped"
        self.log = logger.get_logger(self.name)
        self.n = n * 60
        self.do_run = True
        self._function = function
        self._strip = stripe
        self._name = function if name is None else name

    def _process(self):
        self.log.info(f"Thread '{self._name}' initialized, start process '{self._function}' for {self.n} seconds")
        func_p = Process(target=self._function, name=self._name, args=(self._strip,))
        func_p.start()
        return func_p

    def run(self):
        p = self._process()
        self.threads.append(self)
        while self.__getattribute__('do_run') and self.n > 0:
            self.n -= 1
            time.sleep(1)
        if self.n <= 0:
            from bot import external_request
            self.log.info(f"{self.expired}: {self._function}")
            external_request(standby)
        p.terminate()
        clear(self._strip)
        self._strip.setBrightness(LED_BRIGHTNESS)
        self.threads.remove(self)

    def stop(self):
        self.do_run = False
        self.log.info(f"{self.stopped}: {self._function}")

    @property
    def is_running(self) -> bool:
        return self.do_run


if __name__ == '__main__':
    pass
