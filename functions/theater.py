#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

from neopixel import Color

import logger
from control.led_strip import set_brightness_depending_on_daytime
from functions.effects import color_wipe_full, theater_chase, clear

NAME = "Theater"
LOG = logger.get_logger(NAME)


def run_theater(strip):
    from control import get_stop_flag
    while not get_stop_flag():
        try:
            set_brightness_depending_on_daytime(strip)

            color_wipe_full(strip, Color(127, 0, 0))  # Green wipe
            if not get_stop_flag():
                color_wipe_full(strip, Color(0, 127, 0))  # Red wipe
            if not get_stop_flag():
                color_wipe_full(strip, Color(0, 0, 127))  # Blue wipe
            if not get_stop_flag():
                theater_chase(strip, Color(127, 127, 127))  # White theater chase
            if not get_stop_flag():
                theater_chase(strip, Color(0, 0, 127))  # Blue theater chase
            if not get_stop_flag():
                theater_chase(strip, Color(80, 0, 0))  # Green theater chase

        except KeyboardInterrupt:
            LOG.warn("KeyboardInterrupt")
            exit()

        except Exception as e:
            LOG.error(f"Any error occurs: {e}")
            exit()

    clear(strip)


if __name__ == '__main__':
    pass
