#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import time
from random import uniform

from rpi_ws281x import *

from control.ledstrip import strip_setup
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
            Colorizer.log.debug(f"Setup '{color_key}'.")

    @property
    def all_colors(self):
        return list(self.__colors.keys())

    def __function_loop(self, function):
        Colorizer.log.debug(f"Running {function}")
        from control import get_stop_flag
        while not get_stop_flag():
            function()
        clear(self.__strip)

    def __start(self, color, brightness=None):
        try:
            if brightness is None:
                strip_setup(self.__strip)
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

    def run(self, key, brightness):
        self.__color = self.__colors.get(key)
        self.__start(self.__color, brightness)

    def fade(self):
        def __fade():
            for c in self.all_colors[2:]:
                for i in range(
                        strip_setup(self.__strip)[1]):
                    self.run(c, brightness=i)
                    time.sleep(uniform(0.001, 0.05))
                for i in range(
                        strip_setup(self.__strip)[1]):
                    b = strip_setup(self.__strip)[
                            1] - i
                    self.run(c, brightness=b)
                    time.sleep(uniform(0.001, 0.05))

        self.__function_loop(__fade)

    def switch(self):
        def __switch():
            for c in self.all_colors[2:]:
                self.run(c, None)
                time.sleep(uniform(0.25, 1))

        self.__function_loop(__switch)

    def strobe(self):
        def __strobe():
            self.run('on', 255)
            time.sleep(uniform(0.005, 0.05))
            self.run('off', 0)
            time.sleep(uniform(0.5, 3))

        self.__function_loop(__strobe)


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
    Colorizer(stripe).strobe()


def run_demo(stripe):
    Colorizer(stripe).switch()


def run_demo2(stripe):
    Colorizer(stripe).fade()


if __name__ == '__main__':
    pass
