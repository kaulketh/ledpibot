#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time

import logger
from functions.effects import wheel

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

name = "Rainbow"
log = logger.get_logger(name)


def run_rainbow(strip):
    from control import get_stop_flag
    while not get_stop_flag():
        try:
            strip.setBrightness(40)
            for j in range(256*5):
                if not get_stop_flag():
                    for i in range(strip.numPixels()):
                        if not get_stop_flag():
                            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
                    if not get_stop_flag():
                        strip.show()
                        time.sleep(.02)

        except KeyboardInterrupt:
            log.warn("KeyboardInterrupt")
            exit()
        except Exception as e:
            log.error("Any error occurs: " + str(e))
            exit()


if __name__ == '__main__':
    pass
