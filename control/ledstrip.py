#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import datetime

from neopixel import *

from config import LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_BRIGHTNESS, \
    LED_INVERT, LED_NIGHT_CUT_OFF, \
    LED_MORNING_CUT_OFF, LED_DAY_BRIGHTNESS, \
    LED_NIGHT_BRIGHTNESS
from logger import LOGGER


class Strip:
    name = "LED Strip"

    def __init__(self, count, pin, hz, dma, invert, brightness):
        self.__logger = LOGGER
        self.__count = count
        self.__pin = pin
        self.__hz = hz
        self.__dma = dma
        self.__invert = invert
        self.__brightness = brightness
        self.__logger.debug(f"Create {self}")
        self.__strip = Adafruit_NeoPixel(self.__count, self.__pin, self.__hz,
                                         self.__dma, self.__invert,
                                         self.__brightness)
        self.__logger.debug(f"Initialized: {self.__strip}")
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

    def get_strip(self):
        return self.__strip

    @classmethod
    def setup(cls, s: Adafruit_NeoPixel):
        """
        Low light during given period.

        :param s: Adafruit_NeoPixel
        :return: Datetime, Brightness
        """
        now = datetime.datetime.now()
        if LED_MORNING_CUT_OFF < int(now.hour) < LED_NIGHT_CUT_OFF:
            s.setBrightness(LED_DAY_BRIGHTNESS)
        else:
            s.setBrightness(LED_NIGHT_BRIGHTNESS)
        b = s.getBrightness()
        return now, b


def set_brightness_depending_on_daytime(s: Adafruit_NeoPixel):
    return Strip.setup(s)


STRIP = Strip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,
              LED_BRIGHTNESS).get_strip()

if __name__ == '__main__':
    pass
