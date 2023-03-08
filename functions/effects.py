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


def clear(fairy_lights):
    for i in range(fairy_lights.numPixels()):
        fairy_lights.setPixelColor(i, Color(0, 0, 0))
    fairy_lights.show()


# Define functions which animate LEDs in various ways.
def color_wipe_full(fairy_lights, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(fairy_lights.numPixels()):
        fairy_lights.setPixelColor(i, color)
        fairy_lights.show()
        time.sleep(wait_ms / 1000.0)


def color_wipe(fairy_lights, color, r, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(r):
        fairy_lights.setPixelColor(i, color)
        fairy_lights.show()
        time.sleep(wait_ms / 1000.0)


def theater_chaser(fairy_lights, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, fairy_lights.numPixels(), 3):
                fairy_lights.setPixelColor(i + q, color)
            fairy_lights.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, fairy_lights.numPixels(), 3):
                fairy_lights.setPixelColor(i + q, 0)


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


def rainbow(fairy_lights, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(fairy_lights.numPixels()):
            fairy_lights.setPixelColor(i, wheel((i + j) & 255))
        fairy_lights.show()
        time.sleep(wait_ms / 1000.0)


def rainbow_cycle(light_wreath, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(light_wreath.numPixels()):
            light_wreath.setPixelColor(i, wheel(
                (int(i * 256 / light_wreath.numPixels()) + j) & 255))
        light_wreath.show()
        time.sleep(wait_ms / 1000.0)


def rainbow_chaser(fairy_lights, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, fairy_lights.numPixels(), 3):
                fairy_lights.setPixelColor(i + q, wheel((i + j) % 255))
            fairy_lights.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, fairy_lights.numPixels(), 3):
                fairy_lights.setPixelColor(i + q, 0)


def wipe_second(fairy_lights, color: Color, begin=0, backward=False):
    wait_ms = ((1_000.0 // fairy_lights.numPixels()) // 2) / 1_000.0 \
        if backward else (1_000.0 // fairy_lights.numPixels()) / 1_000.0
    for i in range(begin + 1, fairy_lights.numPixels() + begin):
        if i >= fairy_lights.numPixels():
            i -= fairy_lights.numPixels()
        fairy_lights.setPixelColor(i, color)
        fairy_lights.show()
        time.sleep(wait_ms)
    if backward:
        for i in range(fairy_lights.numPixels() + begin - 1, begin, -1):
            if i >= fairy_lights.numPixels():
                i -= fairy_lights.numPixels()
            fairy_lights.setPixelColor(i, Color(0, 0, 0))
            fairy_lights.show()
            time.sleep(wait_ms)


if __name__ == '__main__':
    pass
