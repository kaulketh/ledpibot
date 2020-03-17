#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

import time

from control.ledstrip import set_brightness_depending_on_daytime
from functions.effects import wheel, clear
from logger import LOGGER as LOG


def run_rainbow(strip):
    from control import get_stop_flag
    while not get_stop_flag():
        try:
            set_brightness_depending_on_daytime(strip)
            for j in range(256 * 5):
                if not get_stop_flag():
                    for i in range(strip.numPixels()):
                        if not get_stop_flag():
                            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
                    if not get_stop_flag():
                        strip.show()
                        time.sleep(.02)

        except KeyboardInterrupt:
            LOG.warn("KeyboardInterrupt")
            exit()
        except Exception as e:
            LOG.error(f"Any error occurs: {e}")
            exit()

    clear(strip)


if __name__ == '__main__':
    pass
