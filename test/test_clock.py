#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

import time

from neopixel import Color

import logger
from control.led_strip import set_brightness_depending_on_daytime, strip
from functions.effects import clear, color_wipe_full

hR = 200
hG = 0
hB = 0

mR = 0
mG = 0
mB = 200

sR = 92
sG = 67
sB = 6

name = "Clock 4"
log = logger.get_logger(name)


def run_clock4(strip):
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
            time.sleep(2)
            color_wipe_full(strip, Color(mG // 4, mR // 4, mB // 4), 20.8)
            clear(strip)




        except KeyboardInterrupt:
            print()
            log.warn("KeyboardInterrupt.")
            exit()

        except Exception as e:
            log.error("Any error occurs: " + str(e))
            exit()

    clear(strip)


def main():
    run_clock4(strip)


if __name__ == '__main__':
    while True:
        main()
