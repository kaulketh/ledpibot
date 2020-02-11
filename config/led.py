#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
LED strip configuration
"""
__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

DAY_BRIGHTNESS = 130
NIGHT_BRIGHTNESS = 30
MORNING_CUT_OFF = 8
NIGHT_CUT_OFF = 18
COUNT = 24  # Number of LED pixels.
PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
DMA = 10  # DMA channel to use for generating signal (try 10)
BRIGHTNESS = 200  # Set to 0 for darkest and 255 for brightest
INVERT = False  # True to invert the signal (when using NPN transistor level shift)
