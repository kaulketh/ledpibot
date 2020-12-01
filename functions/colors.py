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
    logger = LOGGER

    def __init__(self, strip: Adafruit_NeoPixel, color_key=None):
        self.__color = None
        self.__name = self.__class__.__name__
        self.__log = Colorizer.logger
        self.__strip = strip
        self.__div = 3  # to reduce brightness

        if color_key is not None:
            self.set_color(color_key)

        # colors here defined in order R(ed) G(reen) B(lue)
        self.__colors = {
            0: Color(0, 0, 0),
            1: Color(255, 255, 255),
            'red': Color(165 // self.__div, 10 // self.__div,
                         10 // self.__div),
            'blue': Color(0 // self.__div, 50 // self.__div,
                          135 // self.__div),
            'green': Color(0 // self.__div, 135 // self.__div,
                           50 // self.__div),
            'yellow': Color(255 // self.__div, 165 // self.__div,
                            0 // self.__div),
            'orange': Color(210 // self.__div, 70 // self.__div,
                            0 // self.__div),
            'white': Color(255 // (self.__div * 2), 255 // (self.__div * 2),
                           255 // (self.__div * 2)),
            'violet': Color(238 // self.__div, 18 // self.__div,
                            137 // self.__div)
        }

    @property
    def colors(self):
        """ Returns defined colors """
        return self.__colors.keys()

    def set_color(self, color_key):
        self.__color = color_key if isinstance(color_key,
                                               int) else color_key.lower()

    def __get_color(self, key):
        if key in self.colors:
            return self.__colors.get(key)
        else:
            raise Exception(
                f'Key \'{self.__color}\' not defined in {self.__name} colors.')

    def start(self, brightness=None):

        try:
            if self.__color is None:
                raise Exception('Start without set color!')
            else:
                if brightness is None:
                    set_brightness_depending_on_daytime(self.__strip)
                else:
                    self.__strip.setBrightness(brightness)

                for i in range(self.__strip.numPixels()):
                    self.__strip.setPixelColor(i,
                                               self.__get_color(self.__color))
                self.__strip.show()

        except KeyboardInterrupt:
            self.__log.warn("KeyboardInterrupt")
            exit()

        except Exception as e:
            self.__log.error(f"An error occurs: {e}")
            exit()

    @staticmethod
    def run_color(stripe, color_key: str):
        Colorizer.logger.debug(f"running '{color_key.title()}'...")
        from control import get_stop_flag
        while not get_stop_flag():
            Colorizer(stripe, color_key).start()
        clear(stripe)

    @staticmethod
    def all_colors(stripe):
        Colorizer.logger.debug("running...")
        from control import get_stop_flag
        while not get_stop_flag():
            new_strip = Colorizer(stripe)
            for color in new_strip.colors:
                if isinstance(color, str) and not get_stop_flag():
                    new_strip.set_color(color)
                    yield new_strip
                if get_stop_flag():
                    break
        clear(stripe)


def run_red(stripe):
    Colorizer.run_color(stripe, 'red')


def run_blue(stripe):
    Colorizer.run_color(stripe, 'blue')


def run_green(stripe):
    Colorizer.run_color(stripe, 'green')


def run_yellow(stripe):
    Colorizer.run_color(stripe, 'yellow')


def run_orange(stripe):
    Colorizer.run_color(stripe, 'orange')


def run_white(stripe):
    Colorizer.run_color(stripe, 'white')


def run_violet(stripe):
    Colorizer.run_color(stripe, 'violet')


def run_stroboscope(stripe):
    from control import get_stop_flag
    stripe.setBrightness(255)
    Colorizer.logger.debug("running...")
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
    clear(stripe)


def run_demo(stripe):
    for c in Colorizer.all_colors(stripe):
        c.start()
        time.sleep(uniform(0.25, 1))


def run_demo2(stripe):
    for c in Colorizer.all_colors(stripe):
        for i in range(set_brightness_depending_on_daytime(stripe)[1]):
            c.start(brightness=i)
            time.sleep(uniform(0.001, 0.05))
        for i in range(set_brightness_depending_on_daytime(stripe)[1]):
            b = set_brightness_depending_on_daytime(stripe)[1] - i
            c.start(brightness=b)
            time.sleep(uniform(0.001, 0.05))


if __name__ == '__main__':
    pass
