#!/usr/bin/python3
# -*- coding: utf-8 -*-
# based on NeoPixel-60-Ring-Clock of Andy Doro
# https://github.com/andydoro/NeoPixel-60-Ring-Clock

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import inspect
import time

from rpi_ws281x import Color, Adafruit_NeoPixel

from control.wreath import wreath_setup
from functions.color import OwnColors
from functions.effects import clear, wipe_second
from logger import LOGGER


# noinspection PyGlobalUndefined
class Clock:
    log = LOGGER
    REFRESH = .1

    def __init__(self, fairy_lights: Adafruit_NeoPixel, clock: int):
        self.__fairy_lights = fairy_lights
        self.__clock_type = clock
        self.__h_hand = None
        self.__m_hand = None
        self.__s_hand = None
        self.__clock_types = {1: self._one,
                              2: self._two,
                              3: self._three,
                              4: self._four,
                              5: self._five,
                              6: self._six,
                              7: self._seven}

        global __pendulum, __wait_ms, __p_right, __p_left
        __pendulum = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                      13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0]
        __wait_ms = 1 / len(__pendulum)
        __p_left = 0
        __p_right = len(__pendulum) - 1

        Clock.log.debug(
            f"Initialize instance of {self.__class__.__name__} {self}")
        Clock.log.debug(f"Call: {inspect.stack()[1].function}")
        from control import stopped
        while not stopped():
            try:
                self.__h_hand, self.__m_hand, self.__s_hand = self.__hands
                self.__clock_types.get(self.__clock_type)()
            except KeyboardInterrupt:
                Clock.log.warn("KeyboardInterrupt.")
                exit()
            except Exception as e:
                Clock.log.error(f"Any error occurs: {e}")
                exit()
        clear(self.__fairy_lights)

    @property
    def __hands(self):
        _div = 60 / self.__fairy_lights.numPixels()
        now = wreath_setup(self.__fairy_lights)[0]
        seconds_led = int(now.second / _div)
        minutes_led = int(now.minute / _div)
        hours_led = now.hour % 12 * 2
        return hours_led, minutes_led, seconds_led

    def __gic(self, red, green, blue, hand_range, intensity):
        """
        Gradual increase of color intensity of clock hands
        """

        def _color(ints, pixel, r=.0, g=.0, b=.0):
            def color_part(pxl, clr):
                ret = int((pxl + 1) * (ints / (clr + 1)))
                return ret if pxl <= clr else 0

            return Color(color_part(pixel, r) if r > 0 else 0,
                         color_part(pixel, g) if g > 0 else 0,
                         color_part(pixel, b) if b > 0 else 0)

        for i in range(hand_range[0], hand_range[1]):
            c = _color(intensity, i - hand_range[0], red, green, blue)
            self.__fairy_lights.setPixelColor(i % 24, c)

    def __twelfth_hour(self, red, green, blue, *color_of_twelve):
        """
        consider noon or midnight
        """
        self.__gic(red=red, green=green, blue=blue,
                   hand_range=(0, self.__fairy_lights.numPixels()),
                   intensity=100)
        self.__gic(red=color_of_twelve[0],
                   green=color_of_twelve[1],
                   blue=color_of_twelve[2],
                   hand_range=(0, 1),
                   intensity=100)

    def __expanded_minute_hand(self, hour_color, minute_color):
        if self.__m_hand == self.__h_hand:
            if 12 < self.__m_hand < self.__fairy_lights.numPixels():
                if self.__h_hand <= 23:
                    self.__fairy_lights.setPixelColor(self.__h_hand + 1,
                                                      hour_color)
                    self.__fairy_lights.setPixelColor(self.__m_hand,
                                                      minute_color)
                else:
                    self.__fairy_lights.setPixelColor(0, hour_color)
                    self.__fairy_lights.setPixelColor(self.__m_hand - 1,
                                                      minute_color)
            else:
                self.__fairy_lights.setPixelColor(self.__m_hand + 1,
                                                  minute_color)
        else:
            self.__fairy_lights.setPixelColor(self.__m_hand, minute_color)

    def __show_between_6_12(self, hour_color, minute_color, hour_dimmed):
        if 12 < self.__m_hand <= 23:
            self.__fairy_lights.setPixelColor(self.__h_hand, hour_color)
            self.__fairy_lights.setPixelColor(self.__h_hand + 1, hour_dimmed)
        else:
            self.__fairy_lights.setPixelColor(self.__h_hand, hour_color)
        self.__expanded_minute_hand(hour_color, minute_color)
        self.__fairy_lights.show()

    def _one(self):
        for i in range(0, self.__fairy_lights.numPixels(), 1):
            self.__fairy_lights.setPixelColor(self.__h_hand,
                                              OwnColors.color.RED)
            self.__expanded_minute_hand(OwnColors.color.RED,
                                        OwnColors.color.BLUE)
            if i == self.__s_hand:
                self.__fairy_lights.setPixelColor(i, OwnColors.color.YELLOW)
            else:
                self.__fairy_lights.setPixelColor(i, OwnColors.color.OFF)
        self.__fairy_lights.show()
        time.sleep(Clock.REFRESH)

    def _two(self):
        next_minute = self.__m_hand + 1 if self.__m_hand <= 22 else 0
        while not self.__m_hand == next_minute:
            self.__show_between_6_12(OwnColors.color.RED,
                                     OwnColors.color.BLUE,
                                     OwnColors.color.less_intense_red)
            time.sleep(Clock.REFRESH)
            self.__m_hand = self.__hands[1]
        wipe_second(self.__fairy_lights, OwnColors.color.less_intense_blue,
                    self.__m_hand - 1)
        clear(self.__fairy_lights)

    def _three(self):

        def dial(led_wreath):
            _dial = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]  # hours
            # _dial = [0, 6, 12, 18]  # quarter only
            for _l in _dial:
                # warm yellow
                r, g, b = 195, 125, 30
                div = 10
                led_wreath.setPixelColorRGB(_l, r // div, g // div, b // div)

        def hour(led, led_wreath):
            led_wreath.setPixelColor(led, OwnColors.color.RED)

        def set_minute_led_before_and_after(led_wreath, led):
            led_wreath.setPixelColor(led - 1,
                                     OwnColors.color.less_intense_blue)
            led_wreath.setPixelColor(led + 1,
                                     OwnColors.color.less_intense_blue)

        def minute(led, led_hour, led_wreath):
            if led < led_wreath.numPixels():
                if led == led_hour:
                    set_minute_led_before_and_after(led_wreath, led)
                else:
                    led_wreath.setPixelColor(led, OwnColors.color.BLUE)
            if led >= led_wreath.numPixels():
                if led == led_hour:
                    set_minute_led_before_and_after(led_wreath, led_hour)
                    led_wreath.setPixelColor(0, OwnColors.color.BLUE)
                else:
                    led_wreath.setPixelColor(0, OwnColors.color.BLUE)
            else:
                led_wreath.setPixelColor(led, OwnColors.color.BLUE)

        def seconds(leds_per_2500ms, led_wreath):
            for led in range(0, leds_per_2500ms, 1):
                if 0 < (led + 1) < led_wreath.numPixels():
                    led_wreath.setPixelColor(
                        led + 1, OwnColors.color.less_intense_green)
                if (led + 1) == led_wreath.numPixels():
                    led_wreath.setPixelColor(
                        0, OwnColors.color.less_intense_green)

        dial(self.__fairy_lights)
        seconds(self.__s_hand, self.__fairy_lights)
        minute(self.__m_hand, self.__h_hand, self.__fairy_lights)
        hour(self.__h_hand, self.__fairy_lights)

        self.__fairy_lights.show()
        time.sleep(2 * Clock.REFRESH)
        if self.__s_hand == self.__fairy_lights.numPixels():
            time.sleep(13 * Clock.REFRESH)
            clear(self.__fairy_lights)

    def _four(self):
        if self.__h_hand == 0:
            self.__twelfth_hour(0, self.__m_hand, self.__s_hand, 1, 0, 0)
        else:
            self.__gic(red=self.__h_hand,
                       green=self.__m_hand,
                       blue=self.__s_hand,
                       hand_range=(0, self.__fairy_lights.numPixels()),
                       intensity=100)
        self.__fairy_lights.show()
        time.sleep(Clock.REFRESH)

    def _five(self):
        global __pendulum, __p_right, __p_left
        for i in range(len(__pendulum)):
            self.__fairy_lights.setPixelColor(
                __pendulum[i], OwnColors.color.less_intense_yellow)
        if __p_left >= len(__pendulum) - 1:
            if __p_right <= 0:
                __p_right = len(__pendulum) - 1
                __p_left = 0
            else:
                self.__fairy_lights.setPixelColor(
                    __pendulum[__p_right], OwnColors.color.YELLOW)
                __p_right -= 1
        else:
            self.__fairy_lights.setPixelColor(
                __pendulum[__p_left], OwnColors.color.YELLOW)
            __p_left += 1
        self.__show_between_6_12(OwnColors.color.RED,
                                 OwnColors.color.BLUE,
                                 OwnColors.color.less_intense_red)
        global __wait_ms
        time.sleep(__wait_ms)

    def _six(self):
        if self.__h_hand == 0:
            self.__twelfth_hour(0, self.__m_hand, self.__h_hand, 0, 0, 1)
        else:
            self.__gic(red=0,
                       green=self.__m_hand,
                       blue=self.__h_hand,
                       hand_range=(0, self.__fairy_lights.numPixels()),
                       intensity=100)
        self.__fairy_lights.show()
        time.sleep(Clock.REFRESH)

    def _seven(self):
        if self.__h_hand / 2 == 0:
            hour_hand_values = 1, 13
        else:
            hour_hand_values = \
                self.__h_hand / 2, self.__fairy_lights.numPixels()
        if self.__m_hand / 2 == 0:
            minute_hand_values = 1, 1

        else:
            minute_hand_values = self.__m_hand / 2, 12
        self.__gic(red=0, green=0, blue=0,
                   hand_range=(0, self.__fairy_lights.numPixels()),
                   intensity=100)
        m, max_m = minute_hand_values
        self.__gic(red=m, green=m, blue=m,
                   hand_range=(0, max_m),
                   intensity=100)
        h, max_h = hour_hand_values
        self.__gic(red=0, green=h, blue=h,
                   hand_range=(12, max_h),
                   intensity=100)
        self.__fairy_lights.show()
        time.sleep(Clock.REFRESH)


# functions to call the different types of clocks
def run_clock1(led_wreath):
    Clock(led_wreath, 1)


def run_clock2(led_wreath):
    Clock(led_wreath, 2)


def run_clock3(led_wreath):
    Clock(led_wreath, 3)


def run_clock4(led_wreath):
    Clock(led_wreath, 4)


def run_clock5(led_wreath):
    Clock(led_wreath, 5)


def run_clock6(led_wreath):
    Clock(led_wreath, 6)


def run_clock7(led_wreath):
    Clock(led_wreath, 7)


if __name__ == '__main__':
    pass
