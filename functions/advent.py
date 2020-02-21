#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

import time
from datetime import date, timedelta, datetime
from random import randint

from neopixel import Color

import logger
from functions.candles import candle
from functions.effects import theater_chase, clear

name = "Advent"
log = logger.get_logger(name)

# any warm white / no bright yellow
fav_red = 195
fav_green = 150
fav_blue = 50

adv_red = 255
adv_green = 30
adv_blue = 0


# from http://stackoverflow.com/questions/2003870/how-can-i-select-all-of-the-sundays-for-a-year-using-python
# noinspection PyShadowingNames
def _allsundays(year):
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

        # advent = [2, 4, 6, 8, 10, 12, 14, 16]  # uncomment and adapt to test
        day = datetime.now().day
        # day = 22  # uncomment and adapt to test
        # ensure only the day related LEDs are set as candle
        if stripe.numPixels() > day:
            for i in range(day):
                div = randint(randint(6, 8), randint(30, 40))
                # set up different colors for days
                if (i + 1) in advent:
                    stripe.setPixelColor(i, Color(adv_green / div, adv_red / div, adv_blue / div))
                else:
                    stripe.setPixelColor(i, Color(fav_green / div, fav_red / div, fav_blue / div))
                stripe.show()
            time.sleep(0.15)
        else:
            candle(stripe, stripe.numPixels())

    except KeyboardInterrupt:
        log.warn("KeyboardInterrupt")
        exit()

    except Exception as e:
        log.error("Any error occurs: " + str(e))
        exit()


# noinspection PyShadowingNames
def run_advent(strip):
    from control import get_stop_flag
    i = 1
    while not get_stop_flag():
        month = datetime.now().month
        # month = 12  # uncomment to test
        if month == 12:
            _december_cycle(strip, month)
        else:
            while i > 0:
                log.warn('Wrong month for xmas/advent animation, it\'s {0}!'.format(time.strftime("%B")))
                i -= 1
            theater_chase(strip, Color(0, 15, 0))
    clear(strip)


if __name__ == '__main__':
    pass
