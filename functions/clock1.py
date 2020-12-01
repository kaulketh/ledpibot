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
COLOR_MINUTE = Color(0, 0, 200)
COLOR_SECOND = Color(92, 67, 6)


def run_clock1(strip):
    LOGGER.debug("running...")
    from control import get_stop_flag
    while not get_stop_flag():
        # noinspection PyBroadException
        try:
            now = set_brightness_depending_on_daytime(strip)[0]
            hour = int(int(now.hour) % 12 * 2)
            minute = int(now.minute // 2.5)
            second = int(now.second // 2.5)

            for i in range(0, strip.numPixels(), 1):
                # hour
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

                # second
                if i == second:
                    strip.setPixelColor(i, COLOR_SECOND)
                else:
                    strip.setPixelColor(i, Color(0, 0, 0))

            strip.show()
            time.sleep(0.1)
        except KeyboardInterrupt:
            print()
            LOGGER.warn("KeyboardInterrupt.")
            exit()

        except Exception as e:
            LOGGER.error(f"Any error occurs: {e}")
            exit()

    clear(strip)


if __name__ == '__main__':
    pass
