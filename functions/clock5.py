#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

import time

import logger
from control.led_strip import set_brightness_depending_on_daytime
from functions.effects import clear

hR = 200
hG = 0
hB = 0

mR = 0
mG = 0
mB = 200

sR = 92
sG = 67
sB = 6

name = "Clock 5"
log = logger.get_logger(name)


def _all_leds():
    a = [0]
    for i in range(23):
        a.append(i + 1)
    a.append(0)
    return a


pendulum = _all_leds()
wait_ms = 1000 / pendulum.__len__() / 1000


def run_clock5(strip):
    from control import get_stop_flag
    p_left = 0
    p_right = pendulum.__len__() - 1
    while not get_stop_flag():
        try:
            clear(strip)
            now = set_brightness_depending_on_daytime(strip)[0]
            hour = int(int(now.hour) % 12 * 2)
            minute = int(now.minute // 2.5)

            # pendulum of second
            for i in range(pendulum.__len__()):
                strip.setPixelColorRGB(pendulum.__getitem__(i), sG // 4, sR // 4, sB // 4)
            if p_left >= pendulum.__len__() - 1:
                if p_right <= 0:
                    p_right = pendulum.__len__() - 1
                    p_left = 0
                else:
                    strip.setPixelColorRGB(pendulum.__getitem__(p_right), sG, sR, sB)
                    p_right -= 1
            else:
                strip.setPixelColorRGB(pendulum.__getitem__(p_left), sG, sR, sB)
                p_left += 1

            # pointer
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
            time.sleep(wait_ms)

        except KeyboardInterrupt:
            print()
            log.warn("KeyboardInterrupt.")
            exit()
        except Exception as e:
            log.error("Any error occurs: " + str(e))
            exit()
    clear(strip)


if __name__ == '__main__':
    pass
