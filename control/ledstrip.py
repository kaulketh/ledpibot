#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

import datetime

from neopixel import *

from config import LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_BRIGHTNESS, LED_INVERT, LED_NIGHT_CUT_OFF, \
    LED_MORNING_CUT_OFF, LED_DAY_BRIGHTNESS, \
    LED_NIGHT_BRIGHTNESS
from logger import LOGGER


class Strip(object):
    logger = LOGGER
    name = "LED Strip"

    def __init__(self, count, pin, hz, dma, invert, brightness):
        self.count = count
        self.pin = pin
        self.hz = hz
        self.dma = dma
        self.invert = invert
        self.brightness = brightness
        self.logger.debug(f"Create {self}")
        self.strip = Adafruit_NeoPixel(self.count, self.pin, self.hz, self.dma, self.invert, self.brightness)
        self.logger.debug(f"Initialized: {self.strip}")
        self.strip.begin()

    def __repr__(self):
        return(
            f"{self.name}: "
            f"COUNT:{self.count}, "
            f"PIN:{self.pin}, "
            f"FREQ:{self.hz}, "
            f"DMA:{self.dma}, "
            f"INVERT:{self.invert}, "
            f"BRIGHTN.:{self.brightness}")

    def get_instance(self):
        return self.strip


def set_brightness_depending_on_daytime(s: Adafruit_NeoPixel):
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


STRIP = Strip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS).get_instance()

if __name__ == '__main__':
    pass
