#!/usr/bin/python3
# -*- coding: utf-8 -*-
# colors.py
"""
author: Thomas Kaulke, kaulketh@gmail.com
"""

import datetime
import time

from neopixel import Color, Adafruit_NeoPixel

import logger

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
                # Low light during given period
                now = datetime.datetime.now()
                if 8 < int(now.hour) < 18:
                    self.strip.setBrightness(127)
                else:
                    self.strip.setBrightness(50)

                for i in range(self.strip.numPixels()):
                    self.strip.setPixelColor(i, self._get_color(self.color))
                self.strip.show()

        except KeyboardInterrupt:
            self.log.warn("KeyboardInterrupt")
            exit()

        except Exception as e:
            self.log.error("An error occurs: " + str(e))
            # exit()


def run_red(stripe):
    from control import get_stop_flag
    while not get_stop_flag():
        Colorizer(stripe, 'red').start()


def run_blue(stripe):
    from control import get_stop_flag
    while not get_stop_flag():
        Colorizer(stripe, 'blue').start()


def run_green(stripe):
    from control import get_stop_flag
    while not get_stop_flag():
        Colorizer(stripe, 'green').start()


def run_yellow(stripe):
    from control import get_stop_flag
    while not get_stop_flag():
        Colorizer(stripe, 'yellow').start()


def run_orange(stripe):
    from control import get_stop_flag
    while not get_stop_flag():
        Colorizer(stripe, 'orange').start()


def run_white(stripe):
    from control import get_stop_flag
    while not get_stop_flag():
        Colorizer(stripe, 'white').start()


def run_pink(stripe):
    from control import get_stop_flag
    while not get_stop_flag():
        Colorizer(stripe, 'pink').start()


def run_stroboscope(stripe):
    from control import get_stop_flag
    stripe.setBrightness(255)
    while not get_stop_flag():
        Colorizer(stripe, 1).start()
        time.sleep(0.0075)
        Colorizer(stripe, 0).start()
        time.sleep(1)
    Colorizer.clear(stripe)


def run_demo(stripe):
    from control import get_stop_flag
    new_strip = Colorizer(stripe)
    while not get_stop_flag():
        for color in new_strip.colors:
            if isinstance(color, str) and not get_stop_flag():
                new_strip.set_color(color)
                new_strip.start()
            time.sleep(1.5)
            if get_stop_flag():
                break
    new_strip.clear(stripe)


if __name__ == '__main__':
    pass
