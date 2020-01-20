#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from random import randint

from neopixel import Color

import logger
from threads.raspi import RaspberryThread
from functions import cancel, color_wipe_full

name = "Candles"
# any warm white / no bright yellow
red = 195
green = 150
blue = 50


# candle lights from 0 to leds
def candle(strip, leds):
    for i in range(leds):
        div = randint(randint(6, 8), randint(30, 40))
        strip.setPixelColor(i, Color(green / div, red / div, blue / div))
    strip.show()
    time.sleep(0.15)


def run_candles():
    from led_strip import get_strip
    strip = get_strip()
    log.info('candles started')
    try:
        while True:
            candle(strip, strip.numPixels())

    except KeyboardInterrupt:
        log.warn("KeyboardInterrupt")
        exit()

    except Exception as e:
        log.error("Any error occurs: " + str(e))
        exit()

    log.info('candles run stopped')
    color_wipe_full(strip, Color(0, 0, 0), 10)
    log.debug('LED stripe cleared')
    return


def run_thread():
    any(thread.pause() for thread in cancel.threads)
    if not candles_thread.isAlive():
        candles_thread.start()
        print(name + ' thread started')
    candles_thread.resume()
    print(name + ' is running!')
    return


log = logger.get_logger(name)
candles_thread = RaspberryThread(function=run_candles, name=name)
cancel.threads.append(candles_thread)


if __name__ == '__main__':
    pass
