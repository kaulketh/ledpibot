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

    def __init__(self, function, stripe, name=None, n=COUNTDOWN, request_id=None, bot=None):
        super(CountdownThread, self).__init__()
        self._logger = CountdownThread.logger

        self.__bot = bot
        self.__do_run = True
        self.__expired = "Runtime expired"
        self.__stopped = "Stop requested, stopped"
        self.__n = n * 60
        self.__function = function
        self.__strip = stripe
        self.__f_name = function if name is None else name
        self.__chat_id = request_id if request_id is not None else None

    @property
    def __process(self):
        f_process = Process(target=self.__function, name=self.__f_name, args=(self.__strip,))
        f_process.start()
        return f_process

    @property
    def is_running(self) -> bool:
        return self.__do_run

    def run(self):
        self._logger.info(
            f"Thread '{self.__f_name}' initialized from ID:{self.__chat_id}, "
            f"start process '{self.__function}' for {self.__n} seconds")
        p = self.__process
        self.threads.append(self)
        start = self.__n
        while self.__do_run and self.__n > 0:
            self.__n -= 1
            time.sleep(1)
            if self.__n == (start // 2) and self.__n >= 300:
                from bot import LedPiBot
                msg = f"Stop *{self.__f_name}*: T minus *{self.__n // 60}* min."
                self._logger.info(msg.replace("*", ""))
                LedPiBot.external_request(
                    msg, reply_markup=self.__bot.kb_stop, chat_id=self.__chat_id, bot=self.__bot)
                start = self.__n
        if self.__n <= 0:
            from bot import LedPiBot
            self._logger.info(f"{self.__expired}: {self.__function}")
            LedPiBot.external_request(
                standby, reply_markup=self.__bot.kb_markup, chat_id=self.__chat_id, bot=self.__bot)
        p.terminate()
        clear(self.__strip)
        self.__strip.setBrightness(LED_BRIGHTNESS)
        self.threads.remove(self)

    def stop(self):
        self.__do_run = False
        self._logger.info(f"{self.__f_name}: {self.__stopped}: {self.__function}")


if __name__ == '__main__':
    pass
