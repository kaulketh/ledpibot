#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time

import logger
from control.led_strip import set_brightness_depending_on_daytime

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

hR = 200
hG = 0
hB = 0

mR = 0
mG = 0
mB = 200

sR = 92
sG = 67
sB = 6

name = "Clock 2"
log = logger.get_logger(name)


def run_clock2(strip):
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
            log.warn("KeyboardInterrupt.")
            exit()

        except Exception as e:
            log.error("Any error occurs: " + str(e))
            exit()


if __name__ == '__main__':
    pass
