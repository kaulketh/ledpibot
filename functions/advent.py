#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import time
from datetime import date, timedelta, datetime
from random import randint

from rpi_ws281x import *

from functions.candles import candle, RED, BLUE, GREEN
from functions.effects import theater_chase, clear
from logger import LOGGER

candle_red = RED
candle_green = GREEN
candle_blue = BLUE

A_RED = 255
A_GREEN = 30
A_BLUE = 0


# noinspection PyShadowingNames
def _allsundays(year):
    # noinspection LongLine
    """
    http://stackoverflow.com/questions/2003870/how-can-i-select-all-of-the-sundays-for-a-year-using-python
    """
    # start with Nov-27 which is the first possible day of Advent
    # 4 advents == 4 weeks == 28 days -> 25th Dec - 28 day = 27th Nov ;-)

    d = date(year, 11, 27)
    # find the next Sunday after the above date
    d += timedelta(days=6 - d.weekday())
    while d.year == year:
        yield d
        d += timedelta(days=7)


def _december_cycle(stripe, month):
    advent = []
    year = datetime.now().year

    try:
        # collect advent dates
        xmas = date(year, month, 25)
        for d in _allsundays(year):
            if d < xmas:
                advent.append(d.day)

        # advent = [2, 4, 6, 12, 14, 16]  # for testing only
        day = datetime.now().day
        # day = 22  # for testing only
        # ensure only the day related LEDs are set as candle
        if stripe.numPixels() > day:
            for i in range(day):
                # set up different color and brightness per day
                if (i + 1) in advent:
                    p = randint(7, 10) / 100
                    c = Color(int(A_RED * p),
                              int(A_GREEN * p),
                              int(A_BLUE * p))
                    stripe.setPixelColor(i, c)

                else:
                    p = randint(7, 10) / 100
                    c = Color(int(candle_red * p),
                              int(candle_green * p),
                              int(candle_blue * p))
                    stripe.setPixelColor(i, c)
                stripe.show()
            time.sleep(randint(13, 15) / 100)
        else:
            candle(stripe, stripe.numPixels())

    except KeyboardInterrupt:
        LOGGER.warn("KeyboardInterrupt")
        exit()

    except Exception as e:
        LOGGER.error(f"Any error occurs: {e}")
        exit()


# noinspection PyShadowingNames
def run_advent(strip):
    LOGGER.debug("running...")
    from control import get_stop_flag
    i = 1
    while not get_stop_flag():
        month = datetime.now().month
        # month = 1  # for testing only
        if month == 12:
            _december_cycle(strip, month)
        else:
            while i > 0:
                m = time.strftime("%B")
                LOGGER.warn(
                    f"Wrong month for xmas/advent animation, it\'s {m}!")
                i -= 1
            theater_chase(strip, Color(A_RED, A_GREEN, A_BLUE))
    clear(strip)


if __name__ == '__main__':
    pass
