#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import time
from random import randint

from rpi_ws281x import *

from functions.effects import clear
from logger import LOGGER

RED = 255
GREEN = 150
BLUE = 0


def _percent():
    scope = randint(7, 10)
    return scope / 100


# candle lights from 0 to leds
def candle(stripe, leds):
    for i in range(leds):
        p = _percent()
        c = Color(int(RED * p), int(GREEN * p), int(BLUE * p))
        stripe.setPixelColor(i, c)
    stripe.show()
    time.sleep(randint(13, 15) / 100)


def run_candles(strip):
    LOGGER.debug("running...")
    from control import get_stop_flag
    while not get_stop_flag():
        try:
            candle(strip, strip.numPixels())

        except KeyboardInterrupt:
            LOGGER.warn("KeyboardInterrupt")
            exit()

        except Exception as e:
            LOGGER.error(f"Any error occurs: {e}")
            exit()
    clear(strip)


if __name__ == '__main__':
    pass
