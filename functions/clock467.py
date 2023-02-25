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


def _get_watch_hand(strip):
    now = set_brightness_depending_on_daytime(strip)[0]
    second_value = int(now.second / 2.5)
    minute_value = int(now.minute / 2.5)
    hour_value = int(now.hour)
    hour_value = hour_value % 12 * 2
    hour_value = int((hour_value * 24 + minute_value) / 24)
    return hour_value, minute_value, second_value


def _get_color_value(px, watch_hand, intensity) -> int:
    return int(
        (px + 1) * (intensity / (watch_hand + 1)) if px <= watch_hand else 0)


def _clock4(strip):
    hour_value, minute_value, second_value = _get_watch_hand(strip)
    # arc mode
    intensity = 100
    for i in range(strip.numPixels()):
        # calculates a faded arc from low to maximum brightness
        red = _get_color_value(i, hour_value, intensity=intensity)
        green = _get_color_value(i, minute_value, intensity=intensity)
        blue = _get_color_value(i, second_value, intensity=intensity)
        strip.setPixelColor(i % 24,
                            Color(red, green, blue))
    strip.show()
    time.sleep(0.1)


def _clock6(strip):
    hour_value, minute_value = _get_watch_hand(strip)[:2]
    # arc mode
    intensity = 100
    for i in range(strip.numPixels()):
        # calculates a faded arc from low to maximum brightness
        h = _get_color_value(i, hour_value, intensity=intensity)
        m = _get_color_value(i, minute_value, intensity=intensity)
        red, green, blue = 0, m, h
        color = Color(red, green, blue)
        strip.setPixelColor(i % 24, color)
    strip.show()
    time.sleep(0.1)


def _clock7(strip):
    hour, minute = _get_watch_hand(strip)[:2]
    hour_value, minute_value = hour / 2, minute / 2

    intensity = 100
    for i in range(0, 12):
        m = _get_color_value(i, minute_value, intensity=intensity)
        red, green, blue = m, m, m
        color = Color(red, green, blue)
        strip.setPixelColor(i % 24, color)

    for i in range(12, strip.numPixels()):
        h = _get_color_value(i - 12, hour_value, intensity=intensity)
        red, green, blue = 0, h, h
        color = Color(red, green, blue)
        strip.setPixelColor(i % 24, color)
    strip.show()
    time.sleep(0.1)


def _run(strip, clock):
    clocks = {4: _clock4, 6: _clock6, 7: _clock7}
    LOGGER.debug(f"clock{clock} is running ")
    from control import get_stop_flag
    while not get_stop_flag():
        try:
            clocks.get(clock)(strip)
        except KeyboardInterrupt:
            LOGGER.warn("KeyboardInterrupt.")
            exit()

        except Exception as e:
            LOGGER.error(f"Any error occurs: {e}")
            exit()

    clear(strip)


def run_clock4(strip):
    _run(strip, 4)


def run_clock6(strip):
    _run(strip, 6)


def run_clock7(strip):
    _run(strip, 7)


if __name__ == '__main__':
    pass
