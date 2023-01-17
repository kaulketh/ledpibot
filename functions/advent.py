#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import datetime
import time
from random import randint

from rpi_ws281x import *

from functions.candles import BLUE, GREEN, RED
from functions.effects import clear, theater_chase
from logger import LOGGER

# colors
CANDLE = RED, GREEN, BLUE

# advent
A_RED = 255
A_GREEN = 30
A_BLUE = 0
ADVENT = A_RED, A_GREEN, A_BLUE

# first LED
ZERO = 210, 70, 0

# November advent days
NAD = [27, 28, 29, 30]


def __is_advent_period(year):
    return datetime.datetime.now().date() >= datetime.date(year, 11, 27)


def __set_rand_brightness(led, stripe, color):
    p = randint(7, 10) / 100
    c = Color(int(color[0] * p),  # red
              int(color[1] * p),  # green
              int(color[2] * p))  # blue
    stripe.setPixelColor(led, c)


def __allsundays(year):
    # noinspection LongLine,HttpUrlsUsage
    """
    http://stackoverflow.com/questions/2003870/how-can-i-select-all-of-the-sundays-for-a-year-using-python
    """
    # start with Nov-27 which is the first possible day of Advent
    # 4 advents == 4 weeks == 28 days -> 25th Dec - 28 day = 27th Nov ;-)
    d = datetime.date(year, 11, 27)
    # find the next Sunday after the above date
    d += datetime.timedelta(days=6 - d.weekday())
    while d.year == year:
        yield d
        d += datetime.timedelta(days=7)


def __advent_cycle(stripe):
    advents = []

    try:
        # collect advent dates
        year = datetime.datetime.now().year
        for sunday in __allsundays(year):
            if sunday < datetime.date(year, 12, 25):
                advents.append(sunday.day)

        day = datetime.datetime.now().day
        # ensure only the day related LEDs are set as candle
        __show_advent_candles(advents, day, stripe)

    except KeyboardInterrupt:
        LOGGER.warning("KeyboardInterrupt")
        exit()

    except Exception as e:
        LOGGER.error(f"Any error occurs: {e}")
        exit()
    # LOGGER.debug(f"advents: {advents}")


def __show_advent_candles(advent_dates, current_day, led_stripe):
    for i in range(current_day):
        # different color and brightness per day
        # set up first LED as advent because it's before 1st December
        if advent_dates[0] in NAD:
            __set_rand_brightness(0, led_stripe, ZERO)
        # set up other advents in december
        if (i + 1) in advent_dates:
            __set_rand_brightness(i, led_stripe, ADVENT)
        else:
            # set up other days
            __set_rand_brightness(i, led_stripe, CANDLE)
        led_stripe.show()
    time.sleep(randint(13, 15) / 100)


def run_advent(stripe):
    LOGGER.debug("running...")
    from control import get_stop_flag
    i = 1

    while not get_stop_flag():
        year = datetime.datetime.now().year
        if __is_advent_period(year):
            __advent_cycle(stripe)
        else:
            while i > 0:
                LOGGER.warning(
                    f"Wrong period to show xmas/advent animation, "
                    f"it\'s {time.strftime('%A, %d.%B %Y')}!")
                i -= 1
            theater_chase(stripe, Color(ZERO[0], ZERO[1], ZERO[2]))
    clear(stripe)


if __name__ == '__main__':
    pass
