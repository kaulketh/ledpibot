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


def _get_pointer(strip):
    now = set_brightness_depending_on_daytime(strip)[0]
    second_value = int(now.second / 2.5)
    minute_value = int(now.minute / 2.5)
    hour_value = int(now.hour)
    hour_value = hour_value % 12 * 2
    hour_value = int((hour_value * 24 + minute_value) / 24)
    return hour_value, minute_value, second_value


def _get_color_value(px, pointer, intensity) -> int:
    return int((px + 1) * (intensity / (pointer + 1)) if px <= pointer else 0)


def run_clock4(strip):
    LOGGER.debug("running...")
    from control import get_stop_flag
    while not get_stop_flag():
        try:
            hour_value, minute_value, second_value = _get_pointer(strip)
            # arc mode
            intensity = 120
            for i in range(strip.numPixels()):
                # calculates a faded arc from low to maximum brightness
                red = _get_color_value(i, hour_value, intensity=intensity)
                green = _get_color_value(i, minute_value, intensity=intensity)
                blue = _get_color_value(i, second_value, intensity=intensity)
                strip.setPixelColor(i % 24,
                                    Color(red, green, blue))
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
            intensity = 200
            for i in range(strip.numPixels()):
                # calculates a faded arc from low to maximum brightness
                red = _get_color_value(i, hour_value, intensity=intensity)
                green = _get_color_value(i, minute_value, intensity=intensity)
                r = min(red, green)
                g = max(red, green)
                b = (r + g) // 2
                color = Color(r, g, b)
                strip.setPixelColor(i % 24, color)
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
