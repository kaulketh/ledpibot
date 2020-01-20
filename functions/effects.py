#!/usr/bin/python
# -*- coding: utf-8 -*-
# took over from NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#

import time
import argparse

from neopixel import *
from led_strip import get_strip

__author___ = "Tony DiCola"
__email__ = "tony@tonydicola.com"

__maintainer___ = "Thomas Kaulke, kaulketh@gmail.com"
__status__ = "Development"


def clear(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        return True


# Define functions which animate LEDs in various ways.
def color_wipe_full(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


def color_wipe(strip, color, r, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(r):  # strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)
    return


def theater_chase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)


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
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)


def rainbow_cycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)


def theater_chase_rainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
    strip = get_strip()
    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        while True:
            print('Color wipe animations.')
            color_wipe_full(strip, Color(255, 0, 0))  # Green wipe
            color_wipe_full(strip, Color(0, 255, 0))  # Red wipe
            color_wipe_full(strip, Color(0, 0, 255))  # Blue wipe
            print('Theater chase animations.')
            theater_chase(strip, Color(127, 127, 127))  # White theater chase
            theater_chase(strip, Color(127, 0, 0))  # Green theater chase
            theater_chase(strip, Color(0, 0, 127))  # Blue theater chase
            print('Rainbow animations.')
            rainbow(strip)
            rainbow_cycle(strip)
            theater_chase_rainbow(strip)

    except KeyboardInterrupt:
        if args.clear:
            color_wipe_full(strip, Color(0, 0, 0), 10)

    except Exception as e:
        print("Any error occurs: " + str(e))
        exit()
