#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

import time

from neopixel import Color

import logger
from config import CLOCK_HOUR_COLOR, CLOCK_MINUTE_COLOR
from control.led_strip import set_brightness_depending_on_daytime
from functions.effects import clear

NAME = "Clock 2"
LOG = logger.get_logger(NAME)

hR = CLOCK_HOUR_COLOR[0]
hG = CLOCK_HOUR_COLOR[1]
hB = CLOCK_HOUR_COLOR[2]

mR = CLOCK_MINUTE_COLOR[0]
mG = CLOCK_MINUTE_COLOR[1]
mB = CLOCK_MINUTE_COLOR[2]


def run_clock2(strip):
    from control import get_stop_flag
    while not get_stop_flag():
        try:
            hour, minute, next_minute = _get_pointer(strip)
            while not minute == next_minute:
                # hour
                if 12 < minute <= 23:
                    strip.setPixelColorRGB(hour, hG, hR, hB)
                    strip.setPixelColorRGB(hour + 1, hG // 4, hR // 4, hB // 4)
                else:
                    strip.setPixelColorRGB(hour, hG, hR, hB)
                # minute
                if minute == hour:
                    if 12 < minute < strip.numPixels():
                        if hour <= 23:
                            strip.setPixelColorRGB(hour + 1, hG, hR, hB)
                            strip.setPixelColorRGB(minute, mG, mR, mB)
                        else:
                            strip.setPixelColorRGB(0, hG, hR, hB)
                            strip.setPixelColorRGB(minute - 1, mG, mR, mB)
                    else:
                        strip.setPixelColorRGB(minute + 1, mG, mR, mB)
                else:
                    strip.setPixelColorRGB(minute, mG, mR, mB)
                strip.show()
                time.sleep(0.2)
                minute = _get_pointer(strip)[1]
            _wipe_second(strip, (mG // 5, mR // 5, mB // 5), minute - 1, backward=True)
            clear(strip)
        except KeyboardInterrupt:
            print()
            LOG.warn("KeyboardInterrupt.")
            exit()
        except Exception as e:
            LOG.error("Any error occurs: " + str(e))
            exit()
    clear(strip)


def _get_pointer(strip):
    now = set_brightness_depending_on_daytime(strip)[0]
    hour = int(int(now.hour) % 12 * 2)
    minute = int(now.minute // 2.5)
    if minute <= 22:
        next_minute = minute + 1
    else:
        next_minute = 0
    return hour, minute, next_minute


def _wipe_second(stripe, color, begin=0, backward=False):
    if backward:
        wait_ms = ((1000.0 // stripe.numPixels()) // 2) / 1000.0
    else:
        wait_ms = (1000.0 // stripe.numPixels()) / 1000.0

    for i in range(begin + 1, stripe.numPixels() + begin):
        if i >= stripe.numPixels():
            i -= stripe.numPixels()
        stripe.setPixelColor(i, Color(color[0], color[1], color[2]))
        stripe.show()
        time.sleep(wait_ms)
    if backward:
        for i in range(stripe.numPixels() + begin - 1, begin, -1):
            if i >= stripe.numPixels():
                i -= stripe.numPixels()
            stripe.setPixelColor(i, Color(0, 0, 0))
            stripe.show()
            time.sleep(wait_ms)


if __name__ == '__main__':
    pass
