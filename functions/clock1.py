#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import time

from neopixel import *

import logger
from config import DAY_BRIGHTNESS, NIGHT_BRIGHTNESS, MORNING_CUT_OFF, NIGHT_CUT_OFF

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

# color hours
hR = 100
hG = 20
hB = 0

# color minutes
mR = 20
mG = 0
mB = 100

# color seconds
sR = 6
sG = 30
sB = 10

name = "Clock 1"
log = logger.get_logger(name)


def run_clock1(stripe):
    from control import get_stop_flag
    while not get_stop_flag():
        try:
            now = datetime.datetime.now()
            led_for_hour = int(int(now.hour) % 12 * 2)
            led_for_minute = int(now.minute // 2.5)
            leds_per_2500ms = int(round(now.second / 2.5))

            # Low light during given period
            if MORNING_CUT_OFF < int(now.hour) < NIGHT_CUT_OFF:
                stripe.setBrightness(DAY_BRIGHTNESS)
            else:
                stripe.setBrightness(NIGHT_BRIGHTNESS)

            _seconds(leds_per_2500ms, stripe)

            _minute(led_for_minute, led_for_hour, stripe)

            _hour(led_for_hour, stripe)

            stripe.show()
            if leds_per_2500ms == stripe.numPixels():
                time.sleep(1.5)
                _clear(stripe)

        except KeyboardInterrupt:
            log.warn("KeyboardInterrupt.")
            exit()

        except Exception as e:
            log.error("Any error occurs: " + str(e))
            exit()


def _wipe(stripe, wait_ms=50, color=Color(0, 0, 0)):
    for i in range(stripe.numPixels()):
        stripe.setPixelColor(i, color)
        stripe.show()
        time.sleep(wait_ms / 1000.0)


def _clear(stripe):
    for i in range(0, stripe.numPixels()):
        stripe.setPixelColor(i, Color(0, 0, 0))


def _seconds(leds_per_2500ms, stripe):
    for led in range(0, leds_per_2500ms, 1):
        if 0 < (led + 1) < stripe.numPixels():
            stripe.setPixelColorRGB(led + 1, sG, sR, sB)
        if (led + 1) == stripe.numPixels():
            stripe.setPixelColorRGB(0, sG, sR, sB)


def _minute(led, led_hour, stripe):
    if led < stripe.numPixels():
        if led == led_hour:
            _set_minute_led_before_and_after(stripe, led)
        else:
            stripe.setPixelColorRGB(led, mG, mR, mB)
    if led >= stripe.numPixels():
        if led == led_hour:
            _set_minute_led_before_and_after(stripe, led_hour)
            stripe.setPixelColorRGB(0, mG, mR, mB)
        else:
            stripe.setPixelColorRGB(0, mG, mR, mB)
    else:
        stripe.setPixelColorRGB(led, mG, mR, mB)


def _set_minute_led_before_and_after(stripe, led):
    stripe.setPixelColorRGB(led - 1, (mG // 5), (mR // 5), (mB // 5))
    stripe.setPixelColorRGB(led + 1, (mG // 5), (mR // 5), (mB // 5))


def _hour(led, stripe):
    stripe.setPixelColorRGB(led, hG, hR, hB)


if __name__ == '__main__':
    pass
