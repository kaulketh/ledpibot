#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

from multiprocessing import Process
from threading import Thread

from config import LED_BRIGHTNESS, m_stop_f
from functions import clear
from logger import LOGGER


class LightFunction(Thread):
    threads = []
    name = "LightFunction"
    is_clock = False
    SECONDS_PER_DAY = 86_400

    def __init__(self, function, stripe, name=None, request_id=None, bot=None):
        super(LightFunction, self).__init__()
        self._logger = LOGGER

        self.__function = function
        self.__stripe = stripe
        self.__f_name = \
            function.__name__ if name is None else name
        self.__chat_id = request_id
        self.__bot = bot

        self.__do_run = True
        self.__stopped = "Stop requested, stopped"

    @property
    def __process(self):
        f_process = Process(target=self.__function, name=self.__f_name,
                            args=(self.__stripe,))
        f_process.start()
        return f_process

    @property
    def is_running(self) -> bool:
        return self.__do_run

    def run(self):
        self._logger.info(
            f"Initialized '{self.__f_name}' from ID:{self.__chat_id}, "
            f"process: {self.__function}")

        p = self.__process
        LightFunction.threads.append(self)
        import control
        control.open_the_eyes()
        while self.__do_run:
            pass

        # stop
        control.close_the_eyes()
        p.terminate()
        clear(self.__stripe)
        self.__stripe.setBrightness(LED_BRIGHTNESS)
        LightFunction.threads.remove(self)

    def stop(self):
        self.__do_run = False
        self._logger.info(
            f"{self.__f_name}: {self.__stopped}: {self.__function}")
        self.__bot.external_request(m_stop_f.format(self.__f_name),
                                    reply_markup=None,
                                    chat_id=self.__chat_id, bot=self.__bot)


if __name__ == '__main__':
    pass
