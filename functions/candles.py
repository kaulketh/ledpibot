#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from random import randint

from neopixel import Color

import logger

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

from config.led import DAY_BRIGHTNESS, NIGHT_BRIGHTNESS

name = "Candles"
log = logger.get_logger(name)

# any warm white / no bright yellow
red = 195
green = 125
blue = 30


def percent():
    scope = randint(2, 10)
    return scope / 100


def _rand_brightness(stripe, factor=1.0):
    stripe.setBrightness(int(randint(NIGHT_BRIGHTNESS, DAY_BRIGHTNESS) * factor))


# candle lights from 0 to leds
def candle(stripe, leds):
    for turns in range(leds):
        # _rand_brightness(stripe,2)
        for i in range(leds):
            p = percent()
            c = Color(int(green * p), int(red * p), int(blue * p))
            stripe.setPixelColor(i, c)
        stripe.show()
    time.sleep(randint(13, 15) / 100)


def run_candles(strip):
    try:
        candle(strip, strip.numPixels())
        # candle(strip, 12)

    except KeyboardInterrupt:
        log.warn("KeyboardInterrupt")
        exit()

    except Exception as e:
        log.error("Any error occurs: " + str(e))
        exit()


if __name__ == '__main__':
    pass
