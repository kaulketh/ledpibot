#!/usr/bin/python3
# -*- coding: utf-8 -*-
# based on NeoPixel-60-Ring-Clock of Andy Doro
# https://github.com/...
# ...andydoro/NeoPixel-60-Ring-Clock/tree/master/neopixelringclock60

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import time

from rpi_ws281x import *

from control.ledstrip import set_brightness_depending_on_daytime
from functions.effects import clear
from logger import LOGGER

INTENSE = 120
START_PX = 0


def _get_pointer(strip):
    now = set_brightness_depending_on_daytime(strip)[0]
    second_value = int(now.second / 2.5)
    minute_value = int(now.minute / 2.5)
    hour_value = int(now.hour)
    hour_value = hour_value % 12 * 2
    hour_value = int((hour_value * 24 + minute_value) / 24)
    return hour_value, minute_value, second_value


def _get_color_value(px, value, intense=INTENSE):
    return (px + 1) * (intense / (value + 1)) if px <= value else 0


def run_clock4(strip):
    LOGGER.debug("running...")
    from control import get_stop_flag
    while not get_stop_flag():
        try:
            hour_value, minute_value, second_value = _get_pointer(strip)

            # arc mode
            for i in range(strip.numPixels()):
                # calculates a faded arc from low to maximum brightness
                red = _get_color_value(i, hour_value)
                green = _get_color_value(i, minute_value)
                blue = _get_color_value(i, second_value)
                strip.setPixelColor((i + START_PX) % 24,
                                    Color(int(red), int(green), int(blue)))
            strip.show()
            time.sleep(0.1)

        except KeyboardInterrupt:
            LOGGER.warn("KeyboardInterrupt.")
            exit()

        except Exception as e:
            LOGGER.error(f"Any error occurs: {e}")
            exit()

    clear(strip)


def run_clock6(strip):
    LOGGER.debug("running...")
    from control import get_stop_flag
    while not get_stop_flag():
        try:

            hour_value, minute_value = _get_pointer(strip)[:2]

            # arc mode
            for i in range(strip.numPixels()):
                # calculates a faded arc from low to maximum brightness
                red = _get_color_value(i, hour_value)
                green = _get_color_value(i, minute_value)
                r = min(int(red), int(green))
                g = max(int(red), int(green))
                b = (r + g) // 2
                color = Color(r, g, b)
                strip.setPixelColor((i + START_PX) % 24, color)
            strip.show()
            time.sleep(0.1)

        except KeyboardInterrupt:
            LOGGER.warn("KeyboardInterrupt.")
            exit()

        except Exception as e:
            LOGGER.error(f"Any error occurs: {e}")
            exit()

    clear(strip)


if __name__ == '__main__':
    pass
