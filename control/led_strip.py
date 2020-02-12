#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
LED-strip
"""
import datetime

from neopixel import *

import logger
from config import COUNT, PIN, FREQ_HZ, DMA, BRIGHTNESS, INVERT, NIGHT_CUT_OFF, MORNING_CUT_OFF, DAY_BRIGHTNESS, \
    NIGHT_BRIGHTNESS

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
    if MORNING_CUT_OFF < int(now.hour) < NIGHT_CUT_OFF:
        s.setBrightness(DAY_BRIGHTNESS)
    else:
        s.setBrightness(NIGHT_BRIGHTNESS)
    b = s.getBrightness()
    # log.debug('Set brightness to {0}'.format(str(b)))
    return now, b


def get_strip():
    """
    Create NeoPixel object with appropriate configuration and initialize the library.

    :return: NeoPixel/WS281x LED display/strip as s
    """
    log.debug("Create NeoPixel object with appropriate configuration (LED Strip).")
    s = Adafruit_NeoPixel(COUNT, PIN, FREQ_HZ, DMA, INVERT, BRIGHTNESS)
    log.debug("Initialize: " + str(s))
    s.begin()
    return s


strip = get_strip()
