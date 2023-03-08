#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import datetime

from rpi_ws281x import *

from config import LED_BRIGHTNESS, LED_BRIGHTNESS_DAY, LED_BRIGHTNESS_NIGHT, \
    LED_COUNT, LED_CUT_OFF_MORNING, LED_CUT_OFF_NIGHT, LED_DMA, LED_FREQ_HZ, \
    LED_INVERT, LED_PIN
from logger import LOGGER


class LightWreath:
    name = "LED-Light Wreath"
    log = LOGGER

    @classmethod
    def setup(cls, w: Adafruit_NeoPixel):
        """
        Low light during given period.

        :param s: Adafruit_NeoPixel
        :return: Datetime, Brightness
        """
        now = datetime.datetime.now()
        if LED_CUT_OFF_MORNING < int(now.hour) < LED_CUT_OFF_NIGHT:
            w.setBrightness(LED_BRIGHTNESS_DAY)
        else:
            w.setBrightness(LED_BRIGHTNESS_NIGHT)
        b = w.getBrightness()
        return now, b

    def __init__(self, count, pin, hz, dma, invert, brightness):
        self.__count = count
        self.__pin = pin
        self.__hz = hz
        self.__dma = dma
        self.__invert = invert
        self.__brightness = brightness
        LightWreath.log.debug(f"Create {self}")
        self.__strip = Adafruit_NeoPixel(self.__count, self.__pin, self.__hz,
                                         self.__dma, self.__invert,
                                         self.__brightness)
        LightWreath.log.debug(f"Initialized: {self.__strip}")
        self.__strip.begin()

    def __repr__(self):
        return (
            f"{self.name}: "
            f"COUNT:{self.__count}, "
            f"PIN:{self.__pin}, "
            f"FREQ:{self.__hz}, "
            f"DMA:{self.__dma}, "
            f"INVERT:{self.__invert}, "
            f"BRIGHTN.:{self.__brightness}")

    @property
    def wreath(self):
        return self.__strip


def wreath_setup(s: Adafruit_NeoPixel):
    return LightWreath.setup(s)


WREATH = LightWreath(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,
                     LED_BRIGHTNESS).wreath

if __name__ == '__main__':
    pass
