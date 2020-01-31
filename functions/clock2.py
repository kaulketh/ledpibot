#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime

import logger

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
            now = datetime.datetime.now()
            hour = int(int(now.hour) % 12 * 2)
            minute = (int(int(now.minute) / 5 % 12 * 2)) + 1
            second = int(int(now.second) / 2.5)

            # Low light during given period
            if 8 < int(now.hour) < 18:
                strip.setBrightness(127)
            else:
                strip.setBrightness(25)

            for i in range(0, strip.numPixels(), 1):
                # minute
                if hour == minute:
                    strip.setPixelColorRGB(minute + 1, mG, mR, mB)
                    strip.setPixelColorRGB(hour, hG, hR, hB)

                if 12 < minute <= 23:
                    if hour <= 22:
                        strip.setPixelColorRGB(hour + 1, hG, hR, hB)
                        strip.setPixelColorRGB(minute, mG, mR, mB)
                    else:
                        strip.setPixelColorRGB(0, hG, hR, hB)
                        strip.setPixelColorRGB(minute - 1 , mG, mR, mB)
                else:
                    strip.setPixelColorRGB(minute, mG, mR, mB)
                    # hour
                    strip.setPixelColorRGB(hour, hG, hR, hB)


                # second
                if i == second:
                    strip.setPixelColorRGB(i, sG, sR, sB)
                else:
                    strip.setPixelColorRGB(i, 0, 0, 0)

            strip.show()
            # time.sleep(0.1)

        except KeyboardInterrupt:
            print()
            log.warn("KeyboardInterrupt.")
            exit()

        except Exception as e:
            log.error("Any error occurs: " + str(e))
            exit()


if __name__ == '__main__':
    pass
