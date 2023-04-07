#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

LANGUAGE = "en"  # language keys: "de", "en", "fr"

AUTO_REBOOT_ENABLED = False
AUTO_REBOOT_TIME = "01:30"

LED_COUNT = 24  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800_000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 200  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (NPN transistor level shift)
LED_BRIGHTNESS_DAY = 200  # Daytime brightness
LED_BRIGHTNESS_NIGHT = 100  # Night brightness
LED_CUT_OFF_MORNING = 7  # Hour to adjust to day brightness
LED_CUT_OFF_NIGHT = 18  # Hour to adjust to night brightness

if __name__ == '__main__':
    pass
