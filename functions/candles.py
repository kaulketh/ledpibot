#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

import time
from random import randint

from neopixel import Color

import logger
from config.settings import LED_DAY_BRIGHTNESS, LED_NIGHT_BRIGHTNESS
from functions.effects import clear

NAME = "Candles"
LOG = logger.get_logger(NAME)

# any warm white / no bright yellow
red = 195
green = 125
blue = 30


def percent():
    scope = randint(2, 10)
    return scope / 100


def _rand_brightness(stripe, factor=1.0):
    stripe.setBrightness(int(randint(LED_NIGHT_BRIGHTNESS, LED_DAY_BRIGHTNESS) * factor))


# candle lights from 0 to leds
def candle(stripe, leds):
    for turns in range(leds):
        for i in range(leds):
            p = percent()
            c = Color(int(green * p), int(red * p), int(blue * p))
            stripe.setPixelColor(i, c)
        stripe.show()
    time.sleep(randint(13, 15) / 100)


def run_candles(strip):
    from control import get_stop_flag
    while not get_stop_flag():
        try:
            candle(strip, strip.numPixels())

        except KeyboardInterrupt:
            LOG.warn("KeyboardInterrupt")
            exit()

        except Exception as e:
            LOG.error(f"Any error occurs: {e}")
            exit()
    clear(strip)


if __name__ == '__main__':
    pass
