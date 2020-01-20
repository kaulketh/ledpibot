#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
config and init 24-LEDs-strip
"""

from neopixel import *

import logger

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

# LED strip configuration:
LED_COUNT = 24  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 200  # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False

log = logger.get_logger("LED strip")
g_strip = None


def get_strip():
    # Create NeoPixel object with appropriate configuration.
    log.debug("Create NeoPixel object with appropriate configuration.")
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    # Initialize the library (must be called once before other functions).
    log.debug("Initialize the library.")
    strip.begin()
    global g_strip
    g_strip = strip
    return strip
