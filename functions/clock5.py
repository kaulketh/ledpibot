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

COLOR_HOUR = Color(200, 0, 0)
COLOR_HOUR_DIMMED = Color(50, 0, 0)
COLOR_MINUTE = Color(0, 0, 200)
COLOR_SECOND_DIMMED = Color(92 // 4, 67 // 4, 6 // 4)
COLOR_SECOND = Color(92, 67, 6)


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
                strip.setPixelColor(pendulum[i], COLOR_SECOND_DIMMED)
            if p_left >= len(pendulum) - 1:
                if p_right <= 0:
                    p_right = len(pendulum) - 1
                    p_left = 0
                else:
                    strip.setPixelColor(pendulum[p_right], COLOR_SECOND)
                    p_right -= 1
            else:
                strip.setPixelColor(pendulum[p_left], COLOR_SECOND)
                p_left += 1

            # watch hand
            # hour
            if 12 < minute <= 23:
                strip.setPixelColor(hour, COLOR_HOUR)
                strip.setPixelColor(hour + 1, COLOR_HOUR_DIMMED)
            else:
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
