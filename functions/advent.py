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

A_RED = 255
A_GREEN = 30
A_BLUE = 0


def __set_rand_brightness(led, red, green, blue, stripe):
    p = randint(7, 10) / 100
    c = Color(int(red * p),
              int(green * p),
              int(blue * p))
    stripe.setPixelColor(led, c)


def __allsundays(year):
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


def __december_cycle(stripe):
    advent = []
    year = datetime.now().year

    try:
        # collect advent dates
        xmas = date(year, 12, 25)
        for d in __allsundays(year):
            if d < xmas:
                advent.append(d.day)

        day = datetime.now().day
        # ensure only the day related LEDs are set as candle
        if stripe.numPixels() > day:
            for i in range(day):
                # set up different color and brightness per day
                if (i + 1) in advent:
                    __set_rand_brightness(i, A_RED, A_GREEN, A_BLUE, stripe)
                else:
                    __set_rand_brightness(i, RED, GREEN, BLUE, stripe)
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


def run_advent(stripe):
    LOGGER.debug("running...")
    from control import get_stop_flag
    i = 1
    while not get_stop_flag():
        month = datetime.now().month
        if month == 12:
            __december_cycle(stripe)
        else:
            while i > 0:
                m = time.strftime("%B")
                LOGGER.warn(
                    f"Wrong month for xmas/advent animation, it\'s {m}!")
                i -= 1
            theater_chase(stripe, Color(A_RED, A_GREEN, A_BLUE))
    clear(stripe)


if __name__ == '__main__':
    pass
