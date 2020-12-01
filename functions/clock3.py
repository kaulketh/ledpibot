#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import time

from control.ledstrip import set_brightness_depending_on_daytime
from functions.effects import clear
from logger import LOGGER

CLOCK_HOUR_COLOR = (200, 0, 0)
CLOCK_MINUTE_COLOR = (0, 0, 200)
CLOCK_SECOND_COLOR = (92, 67, 6)

CLOCK_HOUR_COLOR_2 = (100, 20, 0)
CLOCK_MINUTE_COLOR_2 = (20, 0, 100)
CLOCK_SECOND_COLOR_2 = (6, 30, 10)

hR = CLOCK_HOUR_COLOR[0]
hG = CLOCK_HOUR_COLOR[1]
hB = CLOCK_HOUR_COLOR[2]

mR = CLOCK_MINUTE_COLOR[0]
mG = CLOCK_MINUTE_COLOR[1]
mB = CLOCK_MINUTE_COLOR[2]

sR = CLOCK_SECOND_COLOR_2[0]
sG = CLOCK_SECOND_COLOR_2[1]
sB = CLOCK_SECOND_COLOR_2[2]


def run_clock3(stripe):
    LOGGER.debug("running...")
    from control import get_stop_flag
    while not get_stop_flag():
        try:

            now = set_brightness_depending_on_daytime(stripe)[0]
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
            stripe.setPixelColorRGB(led + 1, sR, sG, sB)
        if (led + 1) == stripe.numPixels():
            stripe.setPixelColorRGB(0, sR, sG, sB)


def _minute(led, led_hour, stripe):
    if led < stripe.numPixels():
        if led == led_hour:
            _set_minute_led_before_and_after(stripe, led)
        else:
            stripe.setPixelColorRGB(led, mR, mG, mB)
    if led >= stripe.numPixels():
        if led == led_hour:
            _set_minute_led_before_and_after(stripe, led_hour)
            stripe.setPixelColorRGB(0, mR, mG, mB)
        else:
            stripe.setPixelColorRGB(0, mR, mG, mB)
    else:
        stripe.setPixelColorRGB(led, mR, mG, mB)


def _set_minute_led_before_and_after(stripe, led):
    stripe.setPixelColorRGB(led - 1, (mR // 5), (mG // 5), (mB // 5))
    stripe.setPixelColorRGB(led + 1, (mR // 5), (mG // 5), (mB // 5))


def _hour(led, stripe):
    stripe.setPixelColorRGB(led, hR, hG, hB)


def _dial(stripe):
    dial = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]  # hours
    # dial = [0, 6, 12, 18]  # quarter only
    for led in dial:
        stripe.setPixelColorRGB(led, 195 // 10, 125 // 10,
                                30 // 10)  # warm yellow
        # stripe.setPixelColorRGB(led, 15, 15, 15)  # white


if __name__ == '__main__':
    pass
