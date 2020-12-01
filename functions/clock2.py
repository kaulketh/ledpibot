#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import time

from rpi_ws281x import *

from control.ledstrip import set_brightness_depending_on_daytime
from functions.effects import clear
from logger import LOGGER

COLOR_HOUR = Color(200, 0, 0)
COLOR_HOUR_DIMMED = Color(50, 0, 0)
COLOR_MINUTE = Color(0, 0, 200)
COLOR_MINUTE_DIMMED = Color(0, 0, 40)


def run_clock2(strip):
    LOGGER.debug("running...")
    from control import get_stop_flag
    while not get_stop_flag():
        try:
            hour, minute, next_minute = _get_pointer(strip)
            while not minute == next_minute:
                # hour
                if 12 < minute <= 23:
                    strip.setPixelColor(hour, COLOR_HOUR)
                    strip.setPixelColor(hour + 1,
                                        COLOR_HOUR_DIMMED)
                else:
                    strip.setPixelColor(hour, COLOR_HOUR)
                # minute
                if minute == hour:
                    if 12 < minute < strip.numPixels():
                        if hour <= 23:
                            strip.setPixelColor(hour + 1, COLOR_HOUR)
                            strip.setPixelColor(minute, COLOR_MINUTE)
                        else:
                            strip.setPixelColor(0, COLOR_HOUR)
                            strip.setPixelColor(minute - 1, COLOR_MINUTE)
                    else:
                        strip.setPixelColor(minute + 1, COLOR_MINUTE)
                else:
                    strip.setPixelColor(minute, COLOR_MINUTE)
                strip.show()
                time.sleep(0.2)
                minute = _get_pointer(strip)[1]
            _wipe_second(strip, COLOR_MINUTE_DIMMED, minute - 1,
                         backward=True)
            clear(strip)
        except KeyboardInterrupt:
            print()
            LOGGER.warn("KeyboardInterrupt.")
            exit()
        except Exception as e:
            LOGGER.error(f"Any error occurs: {e}")
            exit()
    clear(strip)


def _get_pointer(strip):
    now = set_brightness_depending_on_daytime(strip)[0]
    hour = int(int(now.hour) % 12 * 2)
    minute = int(now.minute // 2.5)
    next_minute = minute + 1 if minute <= 22 else 0
    return hour, minute, next_minute


def _wipe_second(stripe, color: Color, begin=0, backward=False):
    wait_ms = ((1000.0 // stripe.numPixels()) // 2) / 1000.0 \
        if backward else (1000.0 // stripe.numPixels()) / 1000.0

    for i in range(begin + 1, stripe.numPixels() + begin):
        if i >= stripe.numPixels():
            i -= stripe.numPixels()
        stripe.setPixelColor(i, color)
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
