#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

LANGUAGE = "de"
# language keys: "de", "de_emoji", "en", "en_emoji", "fr"
# refer dictionary.py"""

AUTO_REBOOT_ENABLED = False
AUTO_REBOOT_CLOCK_TIME = 2

LED_COUNT = 24  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 200  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (NPN transistor level shift)
LED_DAY_BRIGHTNESS = 170  # Daytime brightness
LED_NIGHT_BRIGHTNESS = 70  # Night brightness
LED_MORNING_CUT_OFF = 7  # Hour to adjust to day brightness
LED_NIGHT_CUT_OFF = 16  # Hour to adjust to night brightness

COUNTDOWN_MINUTES = (8 * 60)  # Max runtime
COUNTDOWN_RESTART_MINUTES = (16 * 60)  # Standby until restart
COUNTDOWN_DISPLAY_REMAINING_RUNTIME = False
COUNTDOWN_MIN_TIME_DISPLAY_REMAINING_RUNTIME = 300

if __name__ == '__main__':
    pass
