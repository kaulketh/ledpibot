#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

import time
from multiprocessing import Process
from threading import Thread

from config import STANDBY_MINUTES as COUNTDOWN, LED_BRIGHTNESS, standby
from functions import clear
from logger import LOGGER


class CountdownThread(Thread):
    threads = []
    name = "Countdown"
    logger = LOGGER

    def __init__(self, function, stripe, name=None, n=COUNTDOWN):
        super(CountdownThread, self).__init__()
        self.expired = "Runtime expired"
        self.stopped = "Stop requested, stopped"
        self.n = n * 60
        self.do_run = True
        self.function = function
        self.strip = stripe
        self.f_name = function if name is None else name

    @property
    def __process(self):
        f_process = Process(target=self.function, name=self.f_name, args=(self.strip,))
        f_process.start()
        return f_process

    def run(self):
        self.logger.info(f"Thread '{self.f_name}' initialized, start process '{self.function}' for {self.n} seconds")
        p = self.__process
        self.threads.append(self)
        start = self.n
        while self.__getattribute__('do_run') and self.n > 0:
            self.n -= 1
            time.sleep(1)
            if self.n == (start // 2) and self.n >= 300:
                from bot import external_request, kb_stop
                msg = f"Stop *{self.f_name}*: T minus *{self.n // 60}* min."
                self.logger.info(msg.replace("*", ""))
                external_request(msg, reply_markup=kb_stop())
                start = self.n
        if self.n <= 0:
            from bot import external_request, kb_markup
            self.logger.info(f"{self.expired}: {self.function}")
            external_request(standby, reply_markup=kb_markup)
        p.terminate()
        clear(self.strip)
        self.strip.setBrightness(LED_BRIGHTNESS)
        self.threads.remove(self)

    def stop(self):
        self.do_run = False
        self.logger.info(f"{self.f_name}: {self.stopped}: {self.function}")

    @property
    def is_running(self) -> bool:
        return self.do_run


if __name__ == '__main__':
    pass
