#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import inspect

from rpi_ws281x import *

from control.light_wreath import wreath_setup
from functions.effects import clear, color_wipe_full, theater_chase
from logger import LOGGER


def run_theater(fairy_lights):
    LOGGER.debug(f"Call: {inspect.stack()[0].function}")
    from control import get_stop_flag
    while not get_stop_flag():
        try:
            wreath_setup(fairy_lights)
            color_wipe_full(fairy_lights, Color(127, 0, 0))  # Red wipe
            if not get_stop_flag():
                color_wipe_full(fairy_lights, Color(0, 127, 0))  # Green wipe
            if not get_stop_flag():
                color_wipe_full(fairy_lights, Color(0, 0, 127))  # Blue wipe
            if not get_stop_flag():
                color_wipe_full(fairy_lights, Color(127, 127, 127))  # White wipe
            if not get_stop_flag():
                theater_chase(fairy_lights,
                              Color(127, 127, 127))  # White theater chase
            if not get_stop_flag():
                theater_chase(fairy_lights, Color(0, 0, 127))  # Blue theater chase
            if not get_stop_flag():
                theater_chase(fairy_lights, Color(0, 127, 0))  # Green theater chase
            if not get_stop_flag():
                theater_chase(fairy_lights, Color(127, 0, 0))  # Red theater chase

        except KeyboardInterrupt:
            LOGGER.warn("KeyboardInterrupt")
            exit()

        except Exception as e:
            LOGGER.error(f"Any error occurs: {e}")
            exit()

    clear(fairy_lights)


if __name__ == '__main__':
    pass
