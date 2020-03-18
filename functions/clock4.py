#!/usr/bin/python3
# -*- coding: utf-8 -*-
# based on NeoPixel-60-Ring-Clock of Andy Doro
# https://github.com/andydoro/NeoPixel-60-Ring-Clock/blob/master/neopixelringclock60/neopixelringclock60.ino

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

import time

from neopixel import Color

from control.ledstrip import set_brightness_depending_on_daytime
from functions.effects import clear
from logger import LOGGER

intense = 120
start_px = 0  # where do we start? shift the arcs if the wiring does not start at the 12


def _wipe(color, strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor((i + start_px) % 24, color)
        strip.show()
        time.sleep(0.05)


def run_clock4(strip):
    from control import get_stop_flag
    while not get_stop_flag():
        try:
            now = set_brightness_depending_on_daytime(strip)[0]
            second_value = int(now.second / 2.5)
            minute_value = int(now.minute / 2.5)
            hour_value = int(now.hour)

            hour_value = hour_value % 12 * 2
            hour_value = int((hour_value * 24 + minute_value) / 24)

            # arc mode
            for i in range(strip.numPixels()):
                # calculates a faded arc from low to maximum brightness
                blue = (i + 1) * (intense / (second_value + 1)) if i <= second_value else 0
                green = (i + 1) * (intense / (minute_value + 1)) if i <= minute_value else 0
                red = (i + 1) * (intense / (hour_value + 1)) if i <= hour_value else 0
                strip.setPixelColor((i + start_px) % 24, Color(int(green), int(red), int(blue)))
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
