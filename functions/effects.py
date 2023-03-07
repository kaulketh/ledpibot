#!/usr/bin/python3
# -*- coding: utf-8 -*-
# taken over from NeoPixel library strandtest example
# origin by Tony DiCola

__author__ = "Thomas Kaulke"
__maintainer__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__status__ = "Production"

import time

from rpi_ws281x import *


def clear(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()


# Define functions which animate LEDs in various ways.
def color_wipe_full(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def color_wipe(strip, color, r, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(r):  # strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theater_chase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def rainbow_cycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel(
                (int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theater_chase_rainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


def wipe_second(strip, color: Color, begin=0, backward=False):
    wait_ms = ((1_000.0 // strip.numPixels()) // 2) / 1_000.0 \
        if backward else (1_000.0 // strip.numPixels()) / 1_000.0
    for i in range(begin + 1, strip.numPixels() + begin):
        if i >= strip.numPixels():
            i -= strip.numPixels()
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms)
    if backward:
        for i in range(strip.numPixels() + begin - 1, begin, -1):
            if i >= strip.numPixels():
                i -= strip.numPixels()
            strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()
            time.sleep(wait_ms)


if __name__ == '__main__':
    pass
