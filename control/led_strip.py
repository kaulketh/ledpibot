#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

import datetime

from neopixel import *

import logger
from config import LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_BRIGHTNESS, LED_INVERT, LED_NIGHT_CUT_OFF, \
    LED_MORNING_CUT_OFF, LED_DAY_BRIGHTNESS, \
    LED_NIGHT_BRIGHTNESS

LOG = logger.get_logger("LED strip")


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


def get_strip():
    """
    Create NeoPixel object with appropriate configuration and initialize the library.

    :return: NeoPixel/WS281x LED display/strip as s
    """
    LOG.debug(
        f"Create LED Strip: "
        f"COUNT:{LED_COUNT}, PIN:{LED_PIN}, FREQ:{LED_FREQ_HZ}, "
        f"DMA:{LED_DMA}, INVERT:{LED_INVERT}, BRIGHTN.:{LED_BRIGHTNESS}")
    s = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    LOG.debug(f"Initialize {s}")
    s.begin()
    return s


strip = get_strip()

if __name__ == '__main__':
    pass
