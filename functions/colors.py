#!/usr/bin/python3
# -*- coding: utf-8 -*-
# colors.py
"""
author: Thomas Kaulke, kaulketh@gmail.com
"""

import datetime

from neopixel import Color

import logger

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

name = "Colors"
log = logger.get_logger(name)

div = 3
# colors defined as G(reen) R(ed) B(lue)
colors = {
    'red': Color(10 // div, 165 // div, 10 // div),
    'blue': Color(50 // div, 0 // div, 135 // div),
    'green': Color(135 // div, 0 // div, 50 // div),
    'yellow': Color(165 // div, 255 // div, 0 // div),
    'orange': Color(70 // div, 210 // div, 0 // div),
    'white': Color(255 // div, 255 // div, 255 // div),
    'pink': Color(25 // div, 135 // div, 25 // div),
}


def _run_color(color, stripe):
    # Low light during given period
    now = datetime.datetime.now()
    if 8 < int(now.hour) < 18:
        stripe.setBrightness(127)
    else:
        stripe.setBrightness(50)

    try:
        for i in range(stripe.numPixels()):
            stripe.setPixelColor(i, colors.get(color))
        stripe.show()

    except KeyboardInterrupt:
        log.warn("KeyboardInterrupt")
        exit()

    except Exception as e:
        log.error("Any error occurs: " + str(e))
        exit()


def run_red(stripe):
    _run_color('red', stripe)


def run_blue(stripe):
    _run_color('blue', stripe)


def run_green(stripe):
    _run_color('green', stripe)


def run_yellow(stripe):
    _run_color('yellow', stripe)


def run_orange(stripe):
    _run_color('orange', stripe)


def run_white(stripe):
    _run_color('white', stripe)


def run_pink(stripe):
    _run_color('pink', stripe)


if __name__ == '__main__':
    pass
