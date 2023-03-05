#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import time

from rpi_ws281x import *

from control.ledstrip import strip_setup
from functions.effects import clear
from logger import LOGGER

COLOR_HOUR = Color(200, 0, 0)
COLOR_MINUTE = Color(0, 0, 200)
COLOR_MINUTE_DIMMED = Color(0, 0, 40)
COLOR_SECOND = Color(6, 30, 10)


def run_clock3(stripe):
    LOGGER.debug("running...")
    from control import get_stop_flag
    while not get_stop_flag():
        try:

            now = strip_setup(stripe)[0]
            led_for_hour = int(int(now.hour) % 12 * 2)
            led_for_minute = int(now.minute // 2.5)
            leds_per_2500ms = int(round(now.second / 2.5))

            _dial(stripe)
            _seconds(leds_per_2500ms, stripe)
            _minute(led_for_minute, led_for_hour, stripe)
            _hour(led_for_hour, stripe)

            stripe.show()
            time.sleep(0.2)
            if leds_per_2500ms == stripe.numPixels():
                time.sleep(1.3)
                clear(stripe)

        except KeyboardInterrupt:
            LOGGER.warn("KeyboardInterrupt.")
            exit()

        except Exception as e:
            LOGGER.error(f"Any error occurs: {e}")
            exit()
    clear(stripe)


def _seconds(leds_per_2500ms, stripe):
    for led in range(0, leds_per_2500ms, 1):
        if 0 < (led + 1) < stripe.numPixels():
            stripe.setPixelColor(led + 1, COLOR_SECOND)
        if (led + 1) == stripe.numPixels():
            stripe.setPixelColor(0, COLOR_SECOND)


def _minute(led, led_hour, stripe):
    if led < stripe.numPixels():
        if led == led_hour:
            _set_minute_led_before_and_after(stripe, led)
        else:
            stripe.setPixelColor(led, COLOR_MINUTE)
    if led >= stripe.numPixels():
        if led == led_hour:
            _set_minute_led_before_and_after(stripe, led_hour)
            stripe.setPixelColor(0, COLOR_MINUTE)
        else:
            stripe.setPixelColor(0, COLOR_MINUTE)
    else:
        stripe.setPixelColor(led, COLOR_MINUTE)


def _set_minute_led_before_and_after(stripe, led):
    stripe.setPixelColor(led - 1, COLOR_MINUTE_DIMMED)
    stripe.setPixelColor(led + 1, COLOR_MINUTE_DIMMED)


def _hour(led, stripe):
    stripe.setPixelColor(led, COLOR_HOUR)


def _dial(stripe):
    dial = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]  # hours
    # dial = [0, 6, 12, 18]  # quarter only
    for led in dial:
        stripe.setPixelColorRGB(led, 195 // 10, 125 // 10,
                                30 // 10)  # warm yellow
        # stripe.setPixelColorRGB(led, 15, 15, 15)  # white


if __name__ == '__main__':
    pass
