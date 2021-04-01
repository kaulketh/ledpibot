#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import time
from datetime import timedelta, datetime
from multiprocessing import Process
from threading import Thread

from config import COUNTDOWN_MINUTES, LED_BRIGHTNESS, m_standby, m_called, \
    m_stop_f, COUNTDOWN_RESTART_MINUTES, \
    COUNTDOWN_DISPLAY_REMAINING_RUNTIME, \
    COUNTDOWN_MIN_TIME_DISPLAY_REMAINING_RUNTIME
from functions import clear
from logger import LOGGER


class Countdown(Thread):
    threads = []
    name = "Countdown"
    is_clock = False
    SECONDS_PER_DAY = 86_400

    def __init__(self, function, stripe, name=None, request_id=None, bot=None):
        super(Countdown, self).__init__()
        self._logger = LOGGER

        self.__function = function
        self.__stripe = stripe
        self.__f_name = \
            function.__name__ if name is None else name
        self.__chat_id = request_id
        self.__bot = bot

        Countdown.is_clock = self.__is_clock = \
            True if function.__name__.find("clock") > -1 else False

        self.__do_run = True
        self.__expired = "Runtime expired"
        self.__stopped = "Stop requested, stopped"

        # disabled countdown for clock functions, should run forever
        # 84_400 seconds per day
        self.__countdown = Countdown.SECONDS_PER_DAY \
            if self.__is_clock else Countdown.countdown_seconds()
        self.__restart = 0 if self.__is_clock else Countdown.restart_seconds()

    @staticmethod
    def recalculated_time(hours: float = 0, minutes: float = 0,
                          seconds: float = 0):
        now = datetime.combine(datetime.today(), datetime.time(datetime.now()))
        now += timedelta(hours=hours, minutes=minutes, seconds=seconds)
        # Emoji unicode
        # https://unicode.org/emoji/charts/full-emoji-list.html#1f609
        # https://unicode.org/emoji/charts/full-emoji-list.html#1f937
        return "\U0001F937 ?\n\U0001F609" \
            if Countdown.is_clock else now.strftime('%H:%M:%S')

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
            f"process: {self.__function} "
            f"until {self.recalculated_time(seconds=self.__countdown)}")
        p = self.__process
        Countdown.threads.append(self)

        # countdown
        start = self.__countdown
        while self.__do_run and self.__countdown > 0:
            self.__countdown -= 1
            time.sleep(1)
            # display remaining runtime
            if COUNTDOWN_DISPLAY_REMAINING_RUNTIME:
                if self.__countdown == (start // 2) \
                        and self.__countdown >= \
                        COUNTDOWN_MIN_TIME_DISPLAY_REMAINING_RUNTIME:
                    msg = f"Stop '{self.__f_name}': " \
                          f"T minus {self.__countdown // 60} min."
                    self._logger.info(msg)
                    self.__bot.external_request(
                        msg, reply_markup=self.__bot.kb_stop_standby,
                        chat_id=self.__chat_id, bot=self.__bot)
                    start = self.__countdown
                elif self.__countdown == (start // 2) \
                        and \
                        self.__countdown >= \
                        COUNTDOWN_MIN_TIME_DISPLAY_REMAINING_RUNTIME:
                    self._logger.debug(
                        f"remaining time of "
                        f"{self.__f_name}: {self.__countdown}")
                    start = self.__countdown
        # runtime expired
        if self.__countdown <= 0 and self.__do_run:
            self._logger.info(f"{self.__expired}: {self.__function}")
            self.__bot.external_request(
                m_standby.format(self.__f_name,
                                 self.recalculated_time(
                                     seconds=self.__restart)),
                reply_markup=self.__bot.kb_stop,
                chat_id=self.__chat_id,
                bot=self.__bot)
            p.terminate()
            clear(self.__stripe)
            self._logger.info(
                f"Standby, "
                f"restart {self.__function} "
                f"at {self.recalculated_time(seconds=self.__restart)}")
            # standby
            while self.__do_run and self.__restart > 0:
                time.sleep(1)
                self.__restart -= 1
            # self restart
            if self.__do_run and self.__restart <= 0:
                self.__countdown = Countdown.countdown_seconds()
                self.__restart = Countdown.restart_seconds()
                self.__bot.external_request(
                    m_called.format(
                        self.__f_name,
                        self.recalculated_time(seconds=self.__countdown)),
                    reply_markup=self.__bot.kb_stop_standby,
                    chat_id=self.__chat_id,
                    bot=self.__bot)
                self.run()
        # stop
        p.terminate()
        clear(self.__stripe)
        self.__stripe.setBrightness(LED_BRIGHTNESS)
        Countdown.threads.remove(self)

    def force_standby(self):
        # disabled standby for clock functions
        # Forced standby for the clock function means an immediate restart
        if self.__is_clock:
            self.__countdown = Countdown.SECONDS_PER_DAY
            self.__restart += 0
            self._logger.info(
                f"Forced standby for the clock function "
                f"means an immediate restart.")
        else:
            self.__countdown = 0
            self.__restart += Countdown.countdown_seconds()
            self._logger.info(
                f"Standby forced for "
                f"{self.__restart // 60} minutes"
                f"({self.__restart // 60 // 60} hours)"
                f", runtime = {self.__countdown}")

    def stop(self):
        self.__do_run = False
        self._logger.info(
            f"{self.__f_name}: {self.__stopped}: {self.__function}")
        self.__bot.external_request(m_stop_f.format(self.__f_name),
                                    reply_markup=None,
                                    chat_id=self.__chat_id, bot=self.__bot)


if __name__ == '__main__':
    pass
