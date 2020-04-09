#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

import time
from datetime import timedelta, datetime
from multiprocessing import Process
from threading import Thread

from config import COUNTDOWN_MINUTES, LED_BRIGHTNESS, m_standby, m_called, \
    COUNTDOWN_RESTART_MINUTES, \
    COUNTDOWN_DISPLAY_REMAINING_TIME
from functions import clear
from logger import LOGGER


class CountdownThread(Thread):
    threads = []
    name = "Countdown"

    def __init__(self, function, stripe, name=None, request_id=None, bot=None):
        super(CountdownThread, self).__init__()
        self._logger = LOGGER

        self.__bot = bot
        self.__do_run = True
        self.__expired = "Runtime expired"
        self.__stopped = "Stop requested, stopped"
        self.__countdown = CountdownThread.countdown_seconds()
        self.__restart = CountdownThread.restart_seconds()
        self.__function = function
        self.__strip = stripe
        self.__f_name = function if name is None else name
        self.__chat_id = request_id if request_id is not None else None

    @staticmethod
    def get_calc_time(hours):
        now = datetime.combine(datetime.today(), datetime.time(datetime.now()))
        now += timedelta(hours=hours)
        return now.strftime('%H:%M')

    @staticmethod
    def countdown_hours():
        return COUNTDOWN_MINUTES // 60

    @staticmethod
    def restart_hours():
        return COUNTDOWN_RESTART_MINUTES // 60

    @staticmethod
    def restart_seconds():
        return COUNTDOWN_RESTART_MINUTES * 60

    @staticmethod
    def countdown_seconds():
        return COUNTDOWN_MINUTES * 60

    @property
    def __report_remaining_time(self):
        return COUNTDOWN_DISPLAY_REMAINING_TIME

    @property
    def __process(self):
        f_process = Process(target=self.__function, name=self.__f_name,
                            args=(self.__strip,))
        f_process.start()
        return f_process

    @property
    def is_running(self) -> bool:
        return self.__do_run

    def run(self):
        self._logger.info(
            f"Thread '{self.__f_name}' initialized from ID:{self.__chat_id}, "
            f"start process '{self.__function}' "
            f"for {self.__countdown} seconds")
        p = self.__process
        self.threads.append(self)

        # countdown
        start = self.__countdown
        while self.__do_run and self.__countdown > 0:
            self.__countdown -= 1
            time.sleep(1)
            # display remaining time
            if self.__countdown == (
                    start // 2) \
                    and self.__countdown >= 300 \
                    and CountdownThread.__report_remaining_time:
                from bot import LedPiBot
                msg = f"Stop *{self.__f_name}*: " \
                      f"T minus *{self.__countdown // 60}* min."
                self._logger.info(msg.replace("*", ""))
                LedPiBot.external_request(
                    msg, reply_markup=self.__bot.kb_stop_standby,
                    chat_id=self.__chat_id, bot=self.__bot)
                start = self.__countdown
            elif self.__countdown == (
                    start // 2) \
                    and self.__countdown >= 300:
                self._logger.debug(
                    f"remaining time of {self.__f_name}: {self.__countdown}")
                start = self.__countdown
        # runtime expired
        if self.__countdown <= 0 and self.__do_run:
            from bot import LedPiBot
            self._logger.info(f"{self.__expired}: {self.__function}")
            LedPiBot.external_request(
                m_standby.format(
                    self.get_calc_time(self.restart_hours())),
                reply_markup=self.__bot.kb_stop,
                chat_id=self.__chat_id,
                bot=self.__bot)
            p.terminate()
            clear(self.__strip)
            self._logger.info(
                f"Standby, "
                f"waiting to restart {self.__function} "
                f"in {CountdownThread.restart_seconds()} seconds")
            # standby
            while self.__do_run and self.__restart > 0:
                time.sleep(1)
                self.__restart -= 1
            # self restart
            if self.__do_run and self.__restart <= 0:
                self.__countdown = CountdownThread.countdown_seconds()
                self.__restart = CountdownThread.restart_seconds()
                LedPiBot.external_request(
                    m_called.format(
                        self.__f_name,
                        self.get_calc_time(self.countdown_hours())),
                    reply_markup=self.__bot.kb_stop_standby,
                    chat_id=self.__chat_id,
                    bot=self.__bot)
                self.run()
        # stop
        p.terminate()
        clear(self.__strip)
        self.__strip.setBrightness(LED_BRIGHTNESS)
        self.threads.remove(self)

    def force_standby(self):
        self.__countdown = 0
        self._logger.info("Manual reset of runtime, standby forced.")

    def stop(self):
        self.__do_run = False
        self._logger.info(
            f"{self.__f_name}: {self.__stopped}: {self.__function}")


if __name__ == '__main__':
    pass
