#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Configurations and settings
"""
__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

LED_COUNT = 24  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 200  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_DAY_BRIGHTNESS = 130
LED_NIGHT_BRIGHTNESS = 50
LED_MORNING_CUT_OFF = 8
LED_NIGHT_CUT_OFF = 18

STANDBY_MINUTES = 0.1 #240
