#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
LED-strip
"""
from neopixel import *

import logger
from config import COUNT, PIN, FREQ_HZ, DMA, BRIGHTNESS, INVERT

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

log = logger.get_logger("LED strip")


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
