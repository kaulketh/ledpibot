#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import inspect
import time

from control.light_wreath import wreath_setup
from functions.effects import wheel, clear
from logger import LOGGER


def run_rainbow(strip):
    LOGGER.debug(f"Call: {inspect.stack()[0].function}")
    from control import get_stop_flag
    while not get_stop_flag():
        try:
            wreath_setup(strip)
            for j in range(256 * 5):
                if not get_stop_flag():
                    for i in range(strip.numPixels()):
                        if not get_stop_flag():
                            strip.setPixelColor(i, wheel(
                                (int(i * 256 / strip.numPixels()) + j) & 255))
                    if not get_stop_flag():
                        strip.show()
                        time.sleep(.02)

        except KeyboardInterrupt:
            LOGGER.warn("KeyboardInterrupt")
            exit()
        except Exception as e:
            LOGGER.error(f"Any error occurs: {e}")
            exit()

    clear(strip)


if __name__ == '__main__':
    pass
