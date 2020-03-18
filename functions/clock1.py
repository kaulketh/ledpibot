#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

import time

from config import CLOCK_HOUR_COLOR, CLOCK_MINUTE_COLOR, CLOCK_SECOND_COLOR
from control.ledstrip import set_brightness_depending_on_daytime
from functions.effects import clear
from logger import LOGGER

hR = CLOCK_HOUR_COLOR[0]
hG = CLOCK_HOUR_COLOR[1]
hB = CLOCK_HOUR_COLOR[2]

mR = CLOCK_MINUTE_COLOR[0]
mG = CLOCK_MINUTE_COLOR[1]
mB = CLOCK_MINUTE_COLOR[2]

sR = CLOCK_SECOND_COLOR[0]
sG = CLOCK_SECOND_COLOR[1]
sB = CLOCK_SECOND_COLOR[2]


def run_clock1(strip):
    from control import get_stop_flag
    while not get_stop_flag():
        # noinspection PyBroadException
        try:
            now = set_brightness_depending_on_daytime(strip)[0]
            hour = int(int(now.hour) % 12 * 2)
            minute = int(now.minute // 2.5)
            second = int(now.second // 2.5)

            for i in range(0, strip.numPixels(), 1):
                # hour
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

                # second
                if i == second:
                    strip.setPixelColorRGB(i, sG, sR, sB)
                else:
                    strip.setPixelColorRGB(i, 0, 0, 0)

            strip.show()
            time.sleep(0.1)

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
