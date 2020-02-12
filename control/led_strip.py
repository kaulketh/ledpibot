#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
LED-strip
"""
import datetime

from neopixel import *

import logger
from config import LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_BRIGHTNESS, LED_INVERT, LED_NIGHT_CUT_OFF, LED_MORNING_CUT_OFF, LED_DAY_BRIGHTNESS, \
    LED_NIGHT_BRIGHTNESS

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

log = logger.get_logger("LED strip")


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
    # log.debug('Set brightness to {0}'.format(str(b)))
    return now, b


def get_strip():
    """
    Create NeoPixel object with appropriate configuration and initialize the library.

    :return: NeoPixel/WS281x LED display/strip as s
    """
    log.debug("Create LED Strip: "
              "COUNT:{0}, PIN:{1}, FREQ:{2}, DMA:{3}, INVERT:{4}, BRIGHTN.:{5}"
              .format(str(LED_COUNT), str(LED_PIN), str(LED_FREQ_HZ), str(LED_DMA), str(LED_INVERT), str(LED_BRIGHTNESS)))
    s = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    log.debug("Initialize " + str(s))
    s.begin()
    return s


strip = get_strip()
