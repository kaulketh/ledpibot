#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import time
from random import randint

from rpi_ws281x import *

from logger import LOGGER


class Candles:
    logger = LOGGER
    RED = 255
    GREEN = 150
    BLUE = 0

    def __init__(self, fairy_lights, led_numbers):
        self.__fairy_lights = fairy_lights
        self.__leds = led_numbers

        Candles.logger.debug(
            f"Initialize instance of {self.__class__.__name__}")
        from control import stopped
        while not stopped():
            try:
                for i in range(self.__leds):
                    percent = randint(7, 10) / 100
                    color = Color(int(Candles.RED * percent),
                                  int(Candles.GREEN * percent),
                                  int(Candles.BLUE * percent))
                    self.__fairy_lights.setPixelColor(i, color)
                self.__fairy_lights.show()
                time.sleep(randint(13, 15) / 100)

            except KeyboardInterrupt:
                Candles.logger.warning("KeyboardInterrupt")
                exit()
            except Exception as e:
                Candles.logger.error(f"Any error occurs: {e}")
                exit()
            finally:
                import control
                control.peripheral_functions.get(3)


def run_candles(light_wreath):
    Candles(light_wreath, light_wreath.numPixels())


if __name__ == '__main__':
    pass
