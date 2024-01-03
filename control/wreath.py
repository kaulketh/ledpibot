#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import datetime

from rpi_ws281x import Adafruit_NeoPixel

from config import led_brightness, led_brightness_day, led_brightness_night, \
    led_count, led_cut_off_morning, led_cut_off_night, led_dma, led_freq_hz, \
    led_invert, led_pin
from logger import LOGGER


class LightWreath:
    name = "LED-Light Wreath"
    log = LOGGER

    @classmethod
    def setup(cls, light_wreath: Adafruit_NeoPixel):
        """
        Low light during given period.
        """
        now = datetime.datetime.now()
        if led_cut_off_morning < int(now.hour) < led_cut_off_night:
            light_wreath.setBrightness(led_brightness_day)
        else:
            light_wreath.setBrightness(led_brightness_night)
        b = light_wreath.getBrightness()
        return now, b

    def __init__(self, count, pin, hz, dma, invert, brightness):
        self.__count = count
        self.__pin = pin
        self.__hz = hz
        self.__dma = dma
        self.__invert = invert
        self.__brightness = brightness
        self.__leds = Adafruit_NeoPixel(self.__count, self.__pin, self.__hz,
                                        self.__dma, self.__invert,
                                        self.__brightness)
        LightWreath.log.debug(
            f"Initialize instance of {self.__class__.__name__} {self}")
        self.__leds.begin()

    def __repr__(self):
        return (
            f"{self.__count}, {self.__pin}, {self.__hz}, "
            f"{self.__dma}, {self.__invert}, {self.__brightness}")

    @property
    def wreath(self):
        return self.__leds


def wreath_setup(light_wreath):
    return LightWreath.setup(light_wreath)


WREATH = LightWreath(led_count, led_pin, led_freq_hz, led_dma, led_invert,
                     led_brightness).wreath

if __name__ == '__main__':
    pass
