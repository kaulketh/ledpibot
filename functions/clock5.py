#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import time

from rpi_ws281x import *

from config import LED_COUNT
from control.ledstrip import set_brightness_depending_on_daytime
from functions.effects import clear
from logger import LOGGER

CLOCK_HOUR_COLOR = (200, 0, 0)
CLOCK_MINUTE_COLOR = (0, 0, 200)
CLOCK_SECOND_COLOR = (92, 67, 6)

hR = CLOCK_HOUR_COLOR[0]
hG = CLOCK_HOUR_COLOR[1]
hB = CLOCK_HOUR_COLOR[2]

mR = CLOCK_MINUTE_COLOR[0]
mG = CLOCK_MINUTE_COLOR[1]
mB = CLOCK_MINUTE_COLOR[2]

sR = CLOCK_SECOND_COLOR[0]
sG = CLOCK_SECOND_COLOR[1]
sB = CLOCK_SECOND_COLOR[2]


def _all_leds():
    a = [0]
    for i in range(LED_COUNT - 1):
        a.append(i + 1)
    a.append(0)
    return a


pendulum = _all_leds()
wait_ms = 1 / len(pendulum)


def run_clock5(strip):
    LOGGER.debug("running...")
    from control import get_stop_flag
    p_left = 0
    p_right = len(pendulum) - 1
    while not get_stop_flag():
        try:
            clear(strip)
            now = set_brightness_depending_on_daytime(strip)[0]
            hour = int(int(now.hour) % 12 * 2)
            minute = int(now.minute // 2.5)

            # pendulum of second
            for i in range(len(pendulum)):
                strip.setPixelColor(pendulum[i],
                                    Color(sR // 4, sG // 4, sB // 4))
            if p_left >= len(pendulum) - 1:
                if p_right <= 0:
                    p_right = len(pendulum) - 1
                    p_left = 0
                else:
                    strip.setPixelColor(pendulum[p_right], Color(sR, sG, sB))
                    p_right -= 1
            else:
                strip.setPixelColor(pendulum[p_left], Color(sR, sG, sB))
                p_left += 1

            # pointer
            # hour
            if 12 < minute <= 23:
                strip.setPixelColor(hour, Color(hR, hG, hB))
                strip.setPixelColor(hour + 1, Color(hR // 4, hG // 4, hB // 4))
            else:
                strip.setPixelColor(hour, Color(hR, hG, hB))
            # minute
            if minute == hour:
                if 12 < minute < strip.numPixels():
                    if hour <= 23:
                        strip.setPixelColor(hour + 1, Color(hR, hG, hB))
                        strip.setPixelColor(minute, Color(mR, mG, mB))
                    else:
                        strip.setPixelColor(0, Color(hR, hG, hB))
                        strip.setPixelColor(minute - 1, Color(mR, mG, mB))
                else:
                    strip.setPixelColor(minute + 1, Color(mR, mG, mB))
            else:
                strip.setPixelColor(minute, Color(mR, mG, mB))

            strip.show()
            time.sleep(wait_ms)

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
