#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import inspect
import time
from random import uniform

from rpi_ws281x import Adafruit_NeoPixel

from control.wreath import wreath_setup
from functions.color import OwnColors
from functions.effects import clear
from logger import LOGGER


class Colorant:
    log = LOGGER

    def __init__(self, fairy_lights: Adafruit_NeoPixel, color_key=None):
        self.__fairy_lights = fairy_lights
        self.__color_keys = [k for k in list(OwnColors.color.keys()) if
                             k != "OFF"]
        Colorant.log.debug(
            f"Initialize instance of {self.__class__.__name__} {self}")
        if color_key is not None:
            Colorant.log.debug(f"Run color '{color_key}'")
            self.run(color_key, None)
        else:
            Colorant.log.debug(
                f"Call function '{inspect.stack()[1].function}'")

    def __loop(self, function):
        Colorant.log.debug(f"Running loop: {inspect.stack()[1].function}")
        from control import stopped
        while not stopped():
            function()
        clear(self.__fairy_lights)

    def __start(self, color, brightness=None):
        try:
            if brightness is None:
                wreath_setup(self.__fairy_lights)
            else:
                self.__fairy_lights.setBrightness(brightness)
            for i in range(self.__fairy_lights.numPixels()):
                self.__fairy_lights.setPixelColor(i, color)
            self.__fairy_lights.show()
        except KeyboardInterrupt:
            Colorant.log.warn("KeyboardInterrupt")
            exit()
        except Exception as e:
            Colorant.log.error(f"An error occurs: {e}")
            exit()

    def run(self, key, brightness):
        self.__start(OwnColors.color.get(key), brightness)

    def fade(self):
        def __fade():
            for c in self.__color_keys:
                for i in range(
                        wreath_setup(self.__fairy_lights)[1]):
                    self.run(c, brightness=i)
                    time.sleep(uniform(0.001, 0.05))
                for i in range(
                        wreath_setup(self.__fairy_lights)[1]):
                    b = wreath_setup(self.__fairy_lights)[
                            1] - i
                    self.run(c, brightness=b)
                    time.sleep(uniform(0.001, 0.05))

        self.__loop(__fade)

    def switch(self):
        def __switch():
            for c in self.__color_keys:
                self.run(c, None)
                time.sleep(uniform(0.25, 1))

        self.__loop(__switch)

    def strobe(self):
        def __strobe():
            self.run('on', 255)
            time.sleep(uniform(0.005, 0.05))
            self.run('off', 0)
            time.sleep(uniform(0.5, 3))

        self.__loop(__strobe)


def run_red(fairy_lights):
    Colorant(fairy_lights, 'red')


def run_blue(fairy_lights):
    Colorant(fairy_lights, 'blue')


def run_green(fairy_lights):
    Colorant(fairy_lights, 'green')


def run_yellow(fairy_lights):
    Colorant(fairy_lights, 'yellow')


def run_orange(fairy_lights):
    Colorant(fairy_lights, 'orange')


def run_white(fairy_lights):
    Colorant(fairy_lights, 'white')


def run_violet(fairy_lights):
    Colorant(fairy_lights, 'violet')


def run_stroboscope(fairy_lights):
    Colorant(fairy_lights).strobe()


def run_demo(fairy_lights):
    Colorant(fairy_lights).switch()


def run_demo2(fairy_lights):
    Colorant(fairy_lights).fade()


if __name__ == '__main__':
    pass
