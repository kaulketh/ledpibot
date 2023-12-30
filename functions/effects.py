#!/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# effects.py
# created 08.03.2023
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# taken over from NeoPixel library strandtest example
# origin by Tony DiCola
# -----------------------------------------------------------
import inspect
import time

from rpi_ws281x import Adafruit_NeoPixel, Color

from control.wreath import wreath_setup
from functions.color import OwnColors
from logger import LOGGER


class Effect:
    log = LOGGER
    spectrum = 255

    def __init__(self, fairy_lights: Adafruit_NeoPixel):
        self.__leds = fairy_lights
        wreath_setup(self.__leds)
        Effect.log.debug(f"Initialize instance of {self.__class__.__name__} "
                         f"for {self.__leds}.")
        Effect.log.debug(str(inspect.stack()[1].code_context[0]).strip())

    @classmethod
    def __wheel(cls, pos):
        """
        color depends on position
        """
        if pos < 85:
            return Color(pos * 3, cls.spectrum - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(cls.spectrum - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, cls.spectrum - pos * 3)

    def clear(self):
        """
        Set color with RGB parts = 0 (zero)
        """
        for i in range(self.__leds.numPixels()):
            self.__leds.setPixelColor(i, OwnColors.color.OFF)
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
        for j in range((Effect.spectrum + 1) * iterations):
            for i in range(self.__leds.numPixels()):
                self.__leds.setPixelColor(i, Effect.__wheel(
                    (i + j) & Effect.spectrum))
            self.__leds.show()
            time.sleep(wait_ms / 1_000.0)

    def rainbow_cycle(self, wait_ms=20, iterations=1):
        """
        Draw rainbow that uniformly distributes itself across all pixels.
        """
        for j in range((Effect.spectrum + 1) * iterations):
            for i in range(self.__leds.numPixels()):
                self.__leds.setPixelColor(
                    i, Effect.__wheel(
                        (int(i * (
                                Effect.spectrum + 1)
                             / self.__leds.numPixels()) + j)
                        & Effect.spectrum))
            self.__leds.show()
            time.sleep(wait_ms / 1_000.0)

    def rainbow_chaser(self, wait_ms=50, iterations=1):
        """
        Rainbow movie theater light style chaser animation.
        """
        for j in range((Effect.spectrum + 1) * iterations):
            for led in range(3):
                for i in range(0, self.__leds.numPixels(), 3):
                    self.__leds.setPixelColor(
                        i + led, Effect.__wheel((i + j) % Effect.spectrum))
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
                self.__leds.setPixelColor(i, OwnColors.color.OFF)
                self.__leds.show()
                time.sleep(wait_ms)


# TODO: create new wipe effects (wandering empty pixel) and implement


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
    while True:
        Effect(wreath).rainbow(iterations=1)


def run_rainbow_cycle(wreath):
    while True:
        Effect(wreath).rainbow_cycle(iterations=1)


def run_rainbow_chaser(wreath):
    while True:
        Effect(wreath).rainbow_chaser(iterations=1)


def run_theater(wreath):
    while True:
        Effect(wreath).full_wipe(OwnColors.color.RED)
        Effect(wreath).full_wipe(OwnColors.color.GREEN)
        Effect(wreath).full_wipe(OwnColors.color.BLUE)
        Effect(wreath).full_wipe(OwnColors.color.WHITE)
        Effect(wreath).chaser(OwnColors.color.WHITE)
        Effect(wreath).chaser(OwnColors.color.BLUE)
        Effect(wreath).chaser(OwnColors.color.GREEN)
        Effect(wreath).chaser(OwnColors.color.RED)


def wipe_second(wreath, color, pivot, back_again=True):
    try:
        Effect(wreath).wipe_second(color, pivot, back_again)
    except KeyboardInterrupt:
        Effect.log.warning("KeyboardInterrupt")
        exit()
    except Exception as e:
        Effect.log.error(f"Any error occurs: {e}")
        exit()


if __name__ == '__main__':
    pass
