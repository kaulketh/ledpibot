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


class Candle:
    logger = LOGGER
    RED = 255
    GREEN = 150
    BLUE = 0

    def __init__(self, fairy_lights, led_numbers):
        self.__fairy_lights = fairy_lights
        self.__leds = led_numbers

        Candle.logger.debug(
            f"Initialize instance of {self.__class__.__name__}")
        from control import get_stop_flag
        while not get_stop_flag():
            try:
                for i in range(self.__leds):
                    percent = randint(7, 10) / 100
                    color = Color(int(Candle.RED * percent),
                                  int(Candle.GREEN * percent),
                                  int(Candle.BLUE * percent))
                    self.__fairy_lights.setPixelColor(i, color)
                self.__fairy_lights.show()
                time.sleep(randint(13, 15) / 100)

            except KeyboardInterrupt:
                Candle.logger.warning("KeyboardInterrupt")
                exit()
            except Exception as e:
                Candle.logger.error(f"Any error occurs: {e}")
                exit()
            finally:
                import control
                control.peripheral_functions.get(3)


def run_candles(light_wreath):
    Candle(light_wreath, light_wreath.numPixels())


if __name__ == '__main__':
    pass
