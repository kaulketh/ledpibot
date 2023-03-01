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
from functions.effects import clear
from logger import LOGGER


class Clock:
    log = LOGGER
    REFRESH = .1
    COLORS = {1: {"hour": Color(200, 0, 0), "minute": Color(0, 0, 200),
                  "second": Color(92, 67, 6)},
              2: {"hour": Color(200, 0, 0), "minute": Color(0, 0, 200),
                  "hour_dimmed": Color(50, 0, 0),
                  "minute_dimmed": Color(0, 0, 40)}
              }

    @classmethod
    def wipe_second(cls, stripe, color: Color, begin=0, backward=False):
        wait_ms = ((1_000.0 // stripe.numPixels()) // 2) / 1_000.0 \
            if backward else (1_000.0 // stripe.numPixels()) / 1_000.0

        for i in range(begin + 1, stripe.numPixels() + begin):
            if i >= stripe.numPixels():
                i -= stripe.numPixels()
            stripe.setPixelColor(i, color)
            stripe.show()
            time.sleep(wait_ms)
        if backward:
            for i in range(stripe.numPixels() + begin - 1, begin, -1):
                if i >= stripe.numPixels():
                    i -= stripe.numPixels()
                stripe.setPixelColor(i, Color(0, 0, 0))
                stripe.show()
                time.sleep(wait_ms)

    @classmethod
    def gradually_increased_color(cls, intensity, pixel, red=.0, green=.0,
                                  blue=.0):

        def gradually_increase(pxl, clr, i=intensity):
            ret = int((pxl + 1) * (i / (clr + 1)))
            return ret if pxl <= clr else 0

        r = gradually_increase(pixel, red) if red > 0 else 0
        g = gradually_increase(pixel, green) if green > 0 else 0
        b = gradually_increase(pixel, blue) if blue > 0 else 0
        return Color(r, g, b)

    def __init__(self, strip: Adafruit_NeoPixel, clock: int):
        self.__clocks = {1: self._one,
                         2: self._two,
                         4: self._four,
                         6: self._six,
                         7: self._seven}
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
                self.__h_hand, self.__m_hand, self.__s_hand = self.__hands
                self.__clocks.get(self.__clock)()
                if self.__clock != 2:
                    self.__strip.show()
                    time.sleep(Clock.REFRESH)
            except KeyboardInterrupt:
                Clock.log.warn("KeyboardInterrupt.")
                exit()
            except Exception as e:
                Clock.log.error(f"Any error occurs: {e}")
                exit()
        clear(self.__strip)

    @property
    def __hands(self):
        now = set_brightness_depending_on_daytime(self.__strip)[0]
        second_value = int(now.second / 2.5)
        minute_value = int(now.minute / 2.5)
        hour_value = int(now.hour)
        hour_value = hour_value % 12 * 2
        hour_value = int((hour_value * 24 + minute_value) / 24)
        return hour_value, minute_value, second_value

    def __gic(self, red, green, blue, hand_range, intensity):
        """
        gradually increased color hands
        """
        for i in range(hand_range[0], hand_range[1]):
            c = Clock.gradually_increased_color(intensity,
                                                i - hand_range[0],
                                                red, green, blue)
            self.__strip.setPixelColor(i % 24, c)

    def __twelfth_hour(self, red, green, blue, *color_of_twelve):
        """
        consider noon or midnight
        """
        self.__gic(red=red, green=green, blue=blue,
                   hand_range=(0, self.__strip.numPixels()),
                   intensity=100)
        self.__gic(red=color_of_twelve[0],
                   green=color_of_twelve[1],
                   blue=color_of_twelve[2],
                   hand_range=(0, 1),
                   intensity=100)

    def __expanded_minute_hand(self, hour_color, minute_color):
        if self.__m_hand == self.__h_hand:
            if 12 < self.__m_hand < self.__strip.numPixels():
                if self.__h_hand <= 23:
                    self.__strip.setPixelColor(self.__h_hand + 1, hour_color)
                    self.__strip.setPixelColor(self.__m_hand, minute_color)
                else:
                    self.__strip.setPixelColor(0, hour_color)
                    self.__strip.setPixelColor(self.__m_hand - 1, minute_color)
            else:
                self.__strip.setPixelColor(self.__m_hand + 1, minute_color)
        else:
            self.__strip.setPixelColor(self.__m_hand, minute_color)

    def _one(self):
        c_h_1 = Clock.COLORS.get(1).get("hour")
        c_m_1 = Clock.COLORS.get(1).get("minute")
        c_s_1 = Clock.COLORS.get(1).get("second")
        for i in range(0, self.__strip.numPixels(), 1):
            self.__strip.setPixelColor(self.__h_hand, c_h_1)  # hour
            self.__expanded_minute_hand(c_h_1, c_m_1)  # minute
            if i == self.__s_hand:  # second
                self.__strip.setPixelColor(i, c_s_1)
            else:
                self.__strip.setPixelColor(i, Color(0, 0, 0))

    def _two(self):
        c_h_2 = Clock.COLORS.get(2).get("hour")
        c_m_2 = Clock.COLORS.get(2).get("minute")
        c_h_2_dimmed = Clock.COLORS.get(2).get("hour_dimmed")
        next_minute = self.__m_hand + 1 if self.__m_hand <= 22 else 0
        while not self.__m_hand == next_minute:
            # hour
            if 12 < self.__m_hand <= 23:
                self.__strip.setPixelColor(self.__h_hand, c_h_2)
                self.__strip.setPixelColor(self.__h_hand + 1, c_h_2_dimmed)
            else:
                self.__strip.setPixelColor(self.__h_hand, c_h_2)
            self.__expanded_minute_hand(c_h_2, c_m_2)  # minute
            self.__strip.show()
            time.sleep(Clock.REFRESH)
            self.__m_hand = self.__hands[1]
        Clock.wipe_second(self.__strip,
                          Clock.COLORS.get(2).get("minute_dimmed"),
                          self.__m_hand - 1, backward=True)
        clear(self.__strip)

    def _four(self):
        if self.__h_hand == 0:
            self.__twelfth_hour(0, self.__m_hand, self.__s_hand, 1, 0, 0)
        else:
            self.__gic(red=self.__h_hand,
                       green=self.__m_hand,
                       blue=self.__s_hand,
                       hand_range=(0, self.__strip.numPixels()),
                       intensity=100)

    def _six(self):
        if self.__h_hand == 0:
            self.__twelfth_hour(0, self.__m_hand, self.__h_hand, 0, 0, 1)
        else:
            self.__gic(red=0,
                       green=self.__m_hand,
                       blue=self.__h_hand,
                       hand_range=(0, self.__strip.numPixels()),
                       intensity=100)

    def _seven(self):
        if self.__h_hand / 2 == 0:
            hour_hand_values = 1, 13
        else:
            hour_hand_values = self.__h_hand / 2, self.__strip.numPixels()
        if self.__m_hand / 2 == 0:
            minute_hand_values = 1, 1
        else:
            minute_hand_values = self.__m_hand / 2, 12
        # right side, minutes, downwards
        m, max_m = minute_hand_values
        self.__gic(red=m, green=m, blue=m,
                   hand_range=(0, max_m),
                   intensity=100)
        # left side, hours, upwards
        h, max_h = hour_hand_values
        self.__gic(red=0, green=h, blue=h,
                   hand_range=(12, max_h),
                   intensity=100)


def run_clock1(strip):
    Clock(strip, 1)


def run_clock2(strip):
    Clock(strip, 2)


def run_clock4(strip):
    Clock(strip, 4)


def run_clock6(strip):
    Clock(strip, 6)


def run_clock7(strip):
    Clock(strip, 7)


if __name__ == '__main__':
    pass
