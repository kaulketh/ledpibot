#!/usr/bin/python3
# -*- coding: utf-8 -*-
# colors.py
"""
author: Thomas Kaulke, kaulketh@gmail.com
"""

import time
from random import uniform

from neopixel import Color, Adafruit_NeoPixel

import logger
from control.led_strip import set_brightness_depending_on_daytime

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"


class Colorizer(object):
    def __init__(self, strip: Adafruit_NeoPixel, color_key=None):
        self.color = None
        self.name = Colorizer.__name__
        self.log = logger.get_logger(self.name)
        self.strip = strip
        self.div = 3  # to reduce brightness

        if color_key is not None:
            # self.log.debug('Init strip with color key \'' + str(color_key) + '\'')
            self.set_color(color_key)
        # else:
        # self.log.debug('Init strip without color key.')

        # colors here defined in order G(reen) R(ed) B(lue)
        self.colors = {
            0: Color(0, 0, 0),
            1: Color(255, 255, 255),
            'red': Color(10 // self.div, 165 // self.div, 10 // self.div),
            'blue': Color(50 // self.div, 0 // self.div, 135 // self.div),
            'green': Color(135 // self.div, 0 // self.div, 50 // self.div),
            'yellow': Color(165 // self.div, 255 // self.div, 0 // self.div),
            'orange': Color(70 // self.div, 210 // self.div, 0 // self.div),
            'white': Color(255 // (self.div * 2), 255 // (self.div * 2), 255 // (self.div * 2)),
            'pink': Color(25 // self.div, 135 // self.div, 25 // self.div),
        }

    def colors(self):
        """ Returns defined colors """
        return self.colors.keys()

    def set_color(self, color_key):
        # self.log.debug('Setup color for key \'' + str(color_key) + '\'')
        if isinstance(color_key, int):
            self.color = color_key
        else:
            self.color = color_key.lower()

    def _get_color(self, key):
        if key in self.colors.keys():
            return self.colors.get(key)
        else:
            raise Exception('Key \'' + str(self.color) + '\' not defined in ' + self.name + '.colors')

    @classmethod
    def clear(cls, strip):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()

    def start(self):
        try:
            if self.color is None:
                raise Exception('Start without set color!')
            else:
                set_brightness_depending_on_daytime(self.strip)

                for i in range(self.strip.numPixels()):
                    self.strip.setPixelColor(i, self._get_color(self.color))
                self.strip.show()

        except KeyboardInterrupt:
            self.log.warn("KeyboardInterrupt")
            exit()

        except Exception as e:
            self.log.error("An error occurs: " + str(e))
            # exit()


def _run_color(stripe, color_key: str):
    from control import get_stop_flag
    while not get_stop_flag():
        Colorizer(stripe, color_key).start()


def _all_colors(stripe):
    from control import get_stop_flag
    while not get_stop_flag():
        new_strip = Colorizer(stripe)
        for color in new_strip.colors:
            if isinstance(color, str) and not get_stop_flag():
                new_strip.set_color(color)
                yield new_strip
            if get_stop_flag():
                break
    Colorizer.clear(stripe)


def run_red(stripe):
    _run_color(stripe, 'red')


def run_blue(stripe):
    _run_color(stripe, 'blue')


def run_green(stripe):
    _run_color(stripe, 'green')


def run_yellow(stripe):
    _run_color(stripe, 'yellow')


def run_orange(stripe):
    _run_color(stripe, 'orange')


def run_white(stripe):
    _run_color(stripe, 'white')


def run_pink(stripe):
    _run_color(stripe, 'pink')


def run_stroboscope(stripe):
    from control import get_stop_flag
    stripe.setBrightness(255)
    while not get_stop_flag():
        Colorizer(stripe, 1).start()
        t = uniform(0.005, 0.05)
        if get_stop_flag():
            break
        time.sleep(t)
        Colorizer(stripe, 0).start()
        t = uniform(0.5, 3)
        if get_stop_flag():
            break
        time.sleep(t)
    Colorizer.clear(stripe)


def run_demo(stripe):
    for c in _all_colors(stripe):
        c.start()
        time.sleep(uniform(0.25, 1))


if __name__ == '__main__':
    pass
