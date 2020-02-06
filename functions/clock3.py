#!/usr/bin/python3
# -*- coding: utf-8 -*-
# based on NeoPixel-60-Ring-Clock of Andy Doro
# https://github.com/andydoro/NeoPixel-60-Ring-Clock/blob/master/neopixelringclock60/neopixelringclock60.ino

import datetime
import time

from neopixel import *
from config import DAYBRIGHTNESS, NIGHTBRIGHTNESS, MORNINGCUTOFF, NIGHTCUTOFF
import logger

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

INTENSE = 120
STARTPIXEL = 0  # where do we start? shift the arcs if the wiring does not start at the 12
name = "Clock 3"
log = logger.get_logger(name)


def _wipe(color, strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor((i + STARTPIXEL) % 24, color)
        strip.show()
        time.sleep(0.05)


def _check_daytime(hour, strip):
    if MORNINGCUTOFF < hour < NIGHTCUTOFF:
        strip.setBrightness(DAYBRIGHTNESS)
    else:
        strip.setBrightness(NIGHTBRIGHTNESS)


def run_clock3(strip):
    from control import get_stop_flag
    while not get_stop_flag():
        try:
            now = datetime.datetime.now()
            second_value = int(now.second / 2.5)
            minute_value = int(now.minute / 2.5)
            hour_value = int(now.hour)
            _check_daytime(hour_value, strip)
            hour_value = hour_value % 12 * 2
            hour_value = int((hour_value * 24 + minute_value) / 24)

            # arc mode
            for i in range(strip.numPixels()):
                if i <= second_value:
                    # calculates a faded arc from low to maximum brightness
                    blue = (i + 1) * (INTENSE / (second_value + 1))
                else:
                    blue = 0

                if i <= minute_value:
                    green = (i + 1) * (INTENSE / (minute_value + 1))
                else:
                    green = 0

                if i <= hour_value:
                    red = (i + 1) * (INTENSE / (hour_value + 1))
                else:
                    red = 0
                strip.setPixelColor((i + STARTPIXEL) % 24, Color(int(green), int(red), int(blue)))

            strip.show()
            time.sleep(0.1)

        except KeyboardInterrupt:
            log.warn("KeyboardInterrupt.")
            exit()

        except Exception as e:
            log.error("Any error occurs: " + str(e))
            exit()


if __name__ == '__main__':
    pass
