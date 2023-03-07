#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import os
import time

from config import IP_MASK_IRONMAN, PORT_MASK_IRONMAN
from logger import LOGGER


class IronMan:
    logger = LOGGER
    IP = IP_MASK_IRONMAN
    PORT = PORT_MASK_IRONMAN

    def __init__(self):
        self.__ip = IronMan.IP
        self.__port = IronMan.PORT
        # noinspection HttpUrlsUsage
        self.__curl = f"curl --silent --output nul " \
                      f"http://{self.__ip}:{self.__port}" \
                      f"/?mode="
        self.__on = "1 &"
        self.__off = "0 &"
        IronMan.logger.debug(
            f"Initialize instance of {self.__class__.__name__}")

    def open(self):
        IronMan.logger.debug("Iron Man opens the eyes.")
        os.system(f"{self.__curl}{self.__on}")

    def close(self):
        IronMan.logger.debug("Iron Man closes the eyes.")
        os.system(f"{self.__curl}{self.__off}")

    def blink(self, times: int, opened: float, closed: float):
        count = times
        IronMan.logger.debug(f"Iron Man {count} times blinks with eyes.")
        while count > 0:
            os.system(f"{self.__curl}{self.__on}")
            time.sleep(opened)
            os.system(f"{self.__curl}{self.__off}")
            time.sleep(closed)
            count -= 1


def close_the_eyes():
    IronMan().close()


def open_the_eyes():
    IronMan().open()


def blink_more_often():
    IronMan().blink(20, .07, .15)


def blink_w_eyes(times=5, opened=.5, closed=.25):
    IronMan().blink(times, opened, closed)


if __name__ == '__main__':
    pass
