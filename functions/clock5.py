#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

import time

import logger
from config import CLOCK_HOUR_COLOR, CLOCK_MINUTE_COLOR, CLOCK_SECOND_COLOR, LED_COUNT
from control.led_strip import set_brightness_depending_on_daytime
from functions.effects import clear

NAME = "Clock 5"
LOG = logger.get_logger(NAME)

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
                strip.setPixelColorRGB(pendulum[i], sG // 4, sR // 4, sB // 4)
            if p_left >= len(pendulum) - 1:
                if p_right <= 0:
                    p_right = len(pendulum) - 1
                    p_left = 0
                else:
                    strip.setPixelColorRGB(pendulum[p_right], sG, sR, sB)
                    p_right -= 1
            else:
                strip.setPixelColorRGB(pendulum[p_left], sG, sR, sB)
                p_left += 1

            # pointer
            # hour
            if 12 < minute <= 23:
                strip.setPixelColorRGB(hour, hG, hR, hB)
                strip.setPixelColorRGB(hour + 1, hG // 4, hR // 4, hB // 4)
            else:
                strip.setPixelColorRGB(hour, hG, hR, hB)
            # minute
            if minute == hour:
                if 12 < minute < strip.numPixels():
                    if hour <= 23:
                        strip.setPixelColorRGB(hour + 1, hG, hR, hB)
                        strip.setPixelColorRGB(minute, mG, mR, mB)
                    else:
                        strip.setPixelColorRGB(0, hG, hR, hB)
                        strip.setPixelColorRGB(minute - 1, mG, mR, mB)
                else:
                    strip.setPixelColorRGB(minute + 1, mG, mR, mB)
            else:
                strip.setPixelColorRGB(minute, mG, mR, mB)

            strip.show()
            time.sleep(wait_ms)

        except KeyboardInterrupt:
            print()
            LOG.warn("KeyboardInterrupt.")
            exit()
        except Exception as e:
            LOG.error("Any error occurs: " + str(e))
            exit()
    clear(strip)


if __name__ == '__main__':
    pass
