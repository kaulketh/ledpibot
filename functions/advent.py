#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import datetime
import time
from random import randint

from rpi_ws281x import Color

from functions.candles import Candles
from functions.effects import Effect
from logger import LOGGER


class Advent:
    logger = LOGGER
    CANDLE = Candles.RED, Candles.GREEN, Candles.BLUE
    ADVENT = 255, 30, 0
    """Advent RGB"""
    FIRST = (210, 70, 0)
    """1st LED RGB"""
    NAD = [27, 28, 29, 30]
    """possible November advent days"""
    WRONG = f"Wrong period to show xmas/advent animation, " \
            f"it\'s {time.strftime('%A, %d.%B %Y')}!"

    @classmethod
    def advent_period(cls, year):
        return datetime.datetime.now().date() >= datetime.date(year, 11, 27)

    @classmethod
    def all_sundays(cls, year):
        # noinspection LongLine,HttpUrlsUsage
        # http://stackoverflow.com/questions/2003870/how-can-i-select-all-of-the-sundays-for-a-year-using-python
        # start with Nov-27 which is the first possible day of Advent
        # 4 advents == 4 weeks == 28 days -> 25th Dec - 28 day = 27th Nov ;-)
        d = datetime.date(year, 11, 27)
        # find the next Sunday after the above date
        d += datetime.timedelta(days=6 - d.weekday())
        while d.year == year:
            yield d
            d += datetime.timedelta(days=7)

    def __init__(self, light_wreath):
        self.__light_wreath = light_wreath
        Advent.logger.debug(
            f"Initialize instance of {self.__class__.__name__} {self}")
        from control import stopped, peripheral_functions
        count = 1
        while not stopped():
            year = datetime.datetime.now().year
            if Advent.advent_period(year):
                self.__calendar()
            else:
                while count > 0:
                    Advent.logger.warning(Advent.WRONG)
                    count -= 1
                Effect(self.__light_wreath).chaser(Color(*Advent.FIRST))
        peripheral_functions.get(3)

    def __calendar(self):
        advents = []
        try:
            # collect advent dates
            year = datetime.datetime.now().year
            for sunday in Advent.all_sundays(year):
                if sunday < datetime.date(year, 12, 25):
                    advents.append(sunday.day)
            day = datetime.datetime.now().day
            # ensure only the day related LEDs are set as candle
            for i in range(day):
                # different color and brightness per day
                # set up first LED as advent because it's before 1st December
                if advents[0] in Advent.NAD:
                    self.__randomize(0, Advent.FIRST)
                # set up other advents in december
                if (i + 1) in advents:
                    self.__randomize(i, Advent.ADVENT)
                else:
                    # set up other days
                    self.__randomize(i, Advent.CANDLE)
                self.__light_wreath.show()
            time.sleep(randint(13, 15) / 100)
        except KeyboardInterrupt:
            Advent.logger.warning("KeyboardInterrupt")
            exit()
        except Exception as e:
            Advent.logger.error(f"Any error occurs: {e}")
            exit()

    def __randomize(self, led, color):
        p = randint(7, 10) / 100
        c = Color(int(color[0] * p),  # red
                  int(color[1] * p),  # green
                  int(color[2] * p))  # blue
        self.__light_wreath.setPixelColor(led, c)


def run_advent(wreath):
    Advent(wreath)


if __name__ == '__main__':
    pass
