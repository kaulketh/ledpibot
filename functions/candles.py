#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from random import randint

from neopixel import Color

import logger

name = "Candles"
log = logger.get_logger(name)

# any warm white / no bright yellow
red = 195
green = 125
blue = 30


def percent():
    scope = randint(3, 10)
    return float(scope) / float(100)


# candle lights from 0 to leds
def candle(stripe, leds):
    for turns in range(leds):
        for i in range(leds):
            p = percent()
            stripe.setPixelColor(i, Color(int(green * p), int(red * p), int(blue * p)))
        stripe.show()
    time.sleep(randint(13, 15) / 100.0)


def run_candles(strip):
    try:
        candle(strip, strip.numPixels())

    except KeyboardInterrupt:
        log.warn("KeyboardInterrupt")
        exit()

    except Exception as e:
        log.error("Any error occurs: " + str(e))
        exit()


if __name__ == '__main__':
    pass
