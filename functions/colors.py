#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import time
from random import uniform

from rpi_ws281x import *

from control.ledstrip import set_brightness_depending_on_daytime
from functions.effects import clear
from logger import LOGGER


class Colorizer:
    log = LOGGER

    @classmethod
    def color(cls, r, g, b, bir=1):
        # bir => brightness/intense reducer
        return Color(r // bir, g // bir, b // bir)

    def __init__(self, strip: Adafruit_NeoPixel, color_key=None):
        self.__strip = strip
        self.__colors = {
            'off': Colorizer.color(0, 0, 0),
            'on': Colorizer.color(255, 255, 255),
            'red': Colorizer.color(165, 10, 10, 3),
            'blue': Colorizer.color(0, 50, 135, 3),
            'green': Colorizer.color(0, 135, 50, 3),
            'yellow': Colorizer.color(255, 165, 0, 3),
            'orange': Colorizer.color(210, 70, 0, 3),
            'white': Colorizer.color(255, 255, 255, 6),
            'violet': Colorizer.color(238, 18, 137, 3)
        }
        self.__color = None
        Colorizer.log.debug(f"Init instance of {self.__class__.__name__}.")
        if color_key is not None:
            self.run(color_key, None)

    def __start(self, color, brightness=None):
        try:
            if brightness is None:
                set_brightness_depending_on_daytime(self.__strip)
            else:
                self.__strip.setBrightness(brightness)
            for i in range(self.__strip.numPixels()):
                self.__strip.setPixelColor(i, color)
            self.__strip.show()
        except KeyboardInterrupt:
            Colorizer.log.warn("KeyboardInterrupt")
            exit()
        except Exception as e:
            Colorizer.log.error(f"An error occurs: {e}")
            exit()

    @property
    def all_colors(self):
        return list(self.__colors.keys())

    def run(self, key, brightness):
        self.__color = self.__colors.get(key)
        self.__start(self.__color, brightness)


def run_red(stripe):
    Colorizer(stripe, 'red')


def run_blue(stripe):
    Colorizer(stripe, 'blue')


def run_green(stripe):
    Colorizer(stripe, 'green')


def run_yellow(stripe):
    Colorizer(stripe, 'yellow')


def run_orange(stripe):
    Colorizer(stripe, 'orange')


def run_white(stripe):
    Colorizer(stripe, 'white')


def run_violet(stripe):
    Colorizer(stripe, 'violet')


def run_stroboscope(stripe):
    from control import get_stop_flag
    strobe = Colorizer(stripe)
    while not get_stop_flag():
        strobe.run('on', 255)
        t = uniform(0.005, 0.05)
        if get_stop_flag():
            break
        time.sleep(t)
        strobe.run('off', 0)
        t = uniform(0.5, 3)
        if get_stop_flag():
            break
        time.sleep(t)
    clear(stripe)


def run_demo(stripe):
    from control import get_stop_flag
    demo = Colorizer(stripe)
    while not get_stop_flag():
        for c in demo.all_colors[2:]:
            demo.run(c, None)
            time.sleep(uniform(0.25, 1))
    clear(stripe)


def run_demo2(stripe):
    from control import get_stop_flag
    demo2 = Colorizer(stripe)
    while not get_stop_flag():
        for c in demo2.all_colors[2:]:
            for i in range(set_brightness_depending_on_daytime(stripe)[1]):
                demo2.run(c, brightness=i)
                time.sleep(uniform(0.001, 0.05))
            for i in range(set_brightness_depending_on_daytime(stripe)[1]):
                b = set_brightness_depending_on_daytime(stripe)[1] - i
                demo2.run(c, brightness=b)
                time.sleep(uniform(0.001, 0.05))
    clear(stripe)


if __name__ == '__main__':
    pass
