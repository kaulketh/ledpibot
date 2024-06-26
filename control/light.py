#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import time
from multiprocessing import Process
from threading import Thread

# noinspection PyUnresolvedReferences
from config import led_brightness, m_stop_f
from functions.effects import clear
from logger import LOGGER


class LightFunction(Thread):
    log = LOGGER
    threads = []
    name = "LightFunction"
    SECONDS_PER_DAY = 86_400

    def __init__(self, function, wreath, name=None, request_id=None, bot=None):
        super(LightFunction, self).__init__()
        self.__function = function
        self.__wreath = wreath
        self.__f_name = \
            function.__name__ if name is None else name
        self.__chat_id = request_id
        self.__bot = bot
        self.__do_run = True
        LightFunction.log.debug(
            f"Initialize instance of {self.__class__.__name__} {self}")

    @property
    def __process(self):
        f_process = Process(target=self.__function, name=self.__f_name,
                            args=(self.__wreath,))
        f_process.start()
        return f_process

    @property
    def is_running(self) -> bool:
        return self.__do_run

    def run(self):
        LightFunction.log.info(f"{self.__f_name} {self.__function}")
        p = self.__process
        LightFunction.threads.append(self)
        while self.__do_run:
            time.sleep(1)
        # stop
        p.terminate()
        clear(self.__wreath)
        self.__wreath.setBrightness(led_brightness)
        LightFunction.threads.remove(self)

    def stop(self):
        self.__do_run = False
        LightFunction.log.debug(f"{self.__f_name} {self.__function}")
        self.__bot.external_request(m_stop_f.format(self.__f_name),
                                    reply_markup=None,
                                    chat_id=self.__chat_id, bot=self.__bot)


if __name__ == '__main__':
    pass
