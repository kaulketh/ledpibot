#!/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# effect.py
# created 08.03.2023
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# taken over from NeoPixel library strandtest example
# origin by Tony DiCola
# -----------------------------------------------------------
import inspect
import time

from rpi_ws281x import *

from control.light_wreath import wreath_setup
from logger import LOGGER


class Effect:
    log = LOGGER
    __spectrum = 255

    def __init__(self, fairy_lights: Adafruit_NeoPixel):
        self.__leds = fairy_lights
        self.__spectrum = Effect.__spectrum
        Effect.log.debug(f"Initialize instance of {self.__class__.__name__} "
                         f"for {self.__leds}.")
        Effect.log.debug(f"Call effect: {inspect.stack()[1].function}")

    @classmethod
    def __wheel(cls, pos):
        """
        Generate rainbow colors across 0-255 positions.
        """
        if pos < 85:
            return Color(pos * 3, cls.__spectrum - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(cls.__spectrum - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, cls.__spectrum - pos * 3)

    def clear(self):
        """
        Set color with RGB parts = 0 (zero)
        """
        for i in range(self.__leds.numPixels()):
            self.__leds.setPixelColor(i, Color(0, 0, 0))
        self.__leds.show()

    def wipe(self, color, length: int = None, wait_ms=50):
        """
        Wipe color across display a pixel at a time.
        """
        num_leds = self.__leds.numPixels() if length is None else length
        for i in range(num_leds):
            self.__leds.setPixelColor(i, color)
            self.__leds.show()
            time.sleep(wait_ms / 1_000.0)

    def full_wipe(self, color, wait_ms=50):
        """
        Wipe color across display a pixel at a time.
        """
        self.wipe(color, wait_ms=wait_ms)

    def chaser(self, color, wait_ms=50, iterations=10):
        """
        Movie theater light style chaser animation.
        """
        for _ in range(iterations):
            for i in range(3):
                for led in range(0, self.__leds.numPixels(), 3):
                    self.__leds.setPixelColor(led + i, color)
                self.__leds.show()
                time.sleep(wait_ms / 1_000.0)
                for led in range(0, self.__leds.numPixels(), 3):
                    self.__leds.setPixelColor(led + i, 0)

    def rainbow(self, wait_ms=20, iterations=1):
        """
        Draw rainbow that fades across all pixels at once.
        """
        for j in range((self.__spectrum + 1) * iterations):
            for i in range(self.__leds.numPixels()):
                self.__leds.setPixelColor(i, Effect.__wheel(
                    (i + j) & self.__spectrum))
            self.__leds.show()
            time.sleep(wait_ms / 1_000.0)

    def rainbow_cycle(self, wait_ms=20, iterations=1):
        """
        Draw rainbow that uniformly distributes itself across all pixels.
        """
        for j in range((self.__spectrum + 1) * iterations):
            for i in range(self.__leds.numPixels()):
                self.__leds.setPixelColor(
                    i, Effect.__wheel(
                        (int(i * 256 / self.__leds.numPixels()) + j)
                        & self.__spectrum))
            self.__leds.show()
            time.sleep(wait_ms / 1_000.0)

    def rainbow_chaser(self, wait_ms=50, iterations=1):
        """
        Rainbow movie theater light style chaser animation.
        """
        for j in range((self.__spectrum + 1) * iterations):
            for led in range(3):
                for i in range(0, self.__leds.numPixels(), 3):
                    self.__leds.setPixelColor(
                        i + led, Effect.__wheel((i + j) % self.__spectrum))
                self.__leds.show()
                time.sleep(wait_ms / 1_000.0)
                for i in range(0, self.__leds.numPixels(), 3):
                    self.__leds.setPixelColor(i + led, 0)

    def wipe_second(self, color: Color, pivot=0, back_again=True):
        """
        Wipes the color in exactly 1 second around the given position,
        whatever the length is and also only forward if desired.
        """
        wait_ms = \
            ((1_000.0 // self.__leds.numPixels()) // 2) / 1_000.0 \
                if back_again \
                else (1_000.0 // self.__leds.numPixels()) / 1_000.0
        for i in range(pivot + 1, self.__leds.numPixels() + pivot):
            if i >= self.__leds.numPixels():
                i -= self.__leds.numPixels()
            self.__leds.setPixelColor(i, color)
            self.__leds.show()
            time.sleep(wait_ms)
        if back_again:
            for i in range(self.__leds.numPixels() + pivot - 1, pivot, -1):
                if i >= self.__leds.numPixels():
                    i -= self.__leds.numPixels()
                self.__leds.setPixelColor(i, Color(0, 0, 0))
                self.__leds.show()
                time.sleep(wait_ms)

    # TODO: create new wipe effects (wandering empty pixel) and implement


def __loop(wreath, effect):
    Effect.log.debug(inspect.stack()[1].code_context)
    from control import get_stop_flag
    while not get_stop_flag():
        try:
            wreath_setup(wreath)
            return effect
        except KeyboardInterrupt:
            Effect.log.warning("KeyboardInterrupt")
            exit()
        except Exception as e:
            Effect.log.error(f"Any error occurs: {e}")
            exit()
    Effect(wreath).clear()


def clear(wreath):
    try:
        Effect(wreath).clear()
    except KeyboardInterrupt:
        Effect.log.warning("KeyboardInterrupt")
        exit()
    except Exception as e:
        Effect.log.error(f"Any error occurs: {e}")
        exit()


def run_rainbow(wreath):
    __loop(wreath, Effect(wreath).rainbow_cycle(iterations=100))


def run_theater(wreath):
    while True:
        __loop(wreath, Effect(wreath).full_wipe(Color(127, 0, 0)))
        __loop(wreath, Effect(wreath).full_wipe(Color(0, 127, 0)))
        __loop(wreath, Effect(wreath).full_wipe(Color(0, 0, 127)))
        __loop(wreath, Effect(wreath).full_wipe(Color(127, 127, 127)))
        __loop(wreath, Effect(wreath).chaser(Color(127, 127, 127)))
        __loop(wreath, Effect(wreath).chaser(Color(0, 0, 127)))
        __loop(wreath, Effect(wreath).chaser(Color(0, 127, 0)))
        __loop(wreath, Effect(wreath).chaser(Color(127, 0, 0)))


def wipe_second(wreath, color, pivot, back_again=True):
    try:
        Effect.wipe_second(wreath, color, pivot, back_again)
    except KeyboardInterrupt:
        Effect.log.warning("KeyboardInterrupt")
        exit()
    except Exception as e:
        Effect.log.error(f"Any error occurs: {e}")
        exit()


if __name__ == '__main__':
    pass
