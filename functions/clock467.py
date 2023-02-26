#!/usr/bin/python3
# -*- coding: utf-8 -*-
# based on NeoPixel-60-Ring-Clock of Andy Doro
# https://github.com/andydoro/NeoPixel-60-Ring-Clock

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import time

from rpi_ws281x import *

from control.ledstrip import set_brightness_depending_on_daytime
from logger import LOGGER


class Clock:
    log = LOGGER
    intensity = 100
    refresh = .1

    @classmethod
    def color_value(cls, pixel, watch_hand):
        ret = int((pixel + 1) * (Clock.intensity / (watch_hand + 1)))
        return ret if pixel <= watch_hand else 0

    @classmethod
    def color(cls, pixel, red=.0, green=.0, blue=.0):
        r = Clock.color_value(pixel, red) if red > 0 else 0
        g = Clock.color_value(pixel, green) if green > 0 else 0
        b = Clock.color_value(pixel, blue) if blue > 0 else 0
        return Color(r, g, b)

    def __init__(self, strip: Adafruit_NeoPixel, clock: int):
        self.__clocks = {4: self.__four, 6: self.__six, 7: self.__seven}
        self.__strip = strip
        self.__clock = clock
        self.__h_hand = None
        self.__m_hand = None
        self.__s_hand = None
        Clock.log.debug(f"Initialize instance of {self.__class__.__name__}"
                        f": Clock {self.__clock} is now running.")
        from control import get_stop_flag
        while not get_stop_flag():
            try:
                self.__h_hand, self.__m_hand, self.__s_hand = self.__hands()
                self.__clocks.get(self.__clock)()
            except KeyboardInterrupt:
                Clock.log.warn("KeyboardInterrupt.")
                exit()
            except Exception as e:
                Clock.log.error(f"Any error occurs: {e}")
                exit()

    def __hands(self):
        now = set_brightness_depending_on_daytime(self.__strip)[0]
        second_value = int(now.second / 2.5)
        minute_value = int(now.minute / 2.5)
        hour_value = int(now.hour)
        hour_value = hour_value % 12 * 2
        hour_value = int((hour_value * 24 + minute_value) / 24)
        return hour_value, minute_value, second_value

    def __color_hands(self, red, green, blue, hand_range):
        for i in range(hand_range[0], hand_range[1]):
            c = Clock.color(i - hand_range[0], red, green, blue)
            self.__strip.setPixelColor(i % 24, c)

    def __show_hands(self):
        self.__strip.show()
        time.sleep(Clock.refresh)

    def __four(self):
        self.__color_hands(red=self.__h_hand,
                           green=self.__m_hand,
                           blue=self.__s_hand,
                           hand_range=(0, self.__strip.numPixels()))
        self.__show_hands()

    def __six(self):
        self.__color_hands(red=0,
                           green=self.__m_hand,
                           blue=self.__h_hand,
                           hand_range=(0, self.__strip.numPixels()))
        self.__show_hands()

    def __seven(self):
        h = self.__h_hand / 2
        m = self.__m_hand / 2
        # right side, minutes, downwards
        self.__color_hands(red=m, green=m, blue=m,
                           hand_range=(0, 12))
        # left side, hours, upwards
        self.__color_hands(red=0, green=h, blue=h,
                           hand_range=(12, self.__strip.numPixels()))
        self.__show_hands()


def run_clock4(strip):
    Clock(strip, 4)


def run_clock6(strip):
    Clock(strip, 6)


def run_clock7(strip):
    Clock(strip, 7)


if __name__ == '__main__':
    pass
