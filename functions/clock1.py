#!/usr/bin/python
# -*- coding: utf-8 -*-

import logger
#import datetime
#import time
# noinspection PyUnresolvedReferences
# from neopixel import *
from threads.raspi import RaspberryThread
from functions import cancel, led_strip


# def color_wipe(strip, color, wait_ms=50):
#     """Wipe color across display a pixel at a time."""
#     for i in range(strip.numPixels()):
#         strip.setPixelColor(i, color)
#         strip.show()
#         time.sleep(wait_ms/1000.0)


# def clear_clock(strip):
#     color_wipe(strip, Color(0, 0, 0), 10)
#     log.info('clock cleared')


# def __run_clock():
#     for i in range(0, strip.numPixels(), 1):
#         strip.setPixelColor(i, Color(0, 0, 0))
#
#     # noinspection PyBroadException
#     try:
#         now = datetime.datetime.now()
#         hour = int(int(now.hour) % 12 * 2)
#         minute = (int(int(now.minute) / 5 % 12 * 2)) + 1
#         second = int(int(now.second) / 2.5)
#
#         # Low light during given period
#         if 8 < int(now.hour) < 18:
#             led_strip.strip.setBrightness(200)
#         else:
#             led_strip.strip.setBrightness(25)
#
#         for i in range(0, led_strip.strip.numPixels(), 1):
#
#             # hour
#             led_strip.strip.setPixelColorRGB(hour, hG, hR, hB)
#
#             # minute
#             if minute == hour:
#                 # TODO doesnt work
#                 led_strip.strip.setPixelColorRGB(minute + 1, mG, mR, mB)
#             else:
#                 led_strip.strip.setPixelColorRGB(minute, mG, mR, mB)
#
#             if minute > 30:
#                 if hour <= 22:
#                     led_strip.strip.setPixelColorRGB(hour + 1, hG, hR, hB)
#                 else:
#                     led_strip.strip.setPixelColorRGB(0, hG, hR, hB)
#
#             # second
#             if i == second:
#                 led_strip.strip.setPixelColorRGB(i, sG, sR, sB)
#             else:
#                 led_strip.strip.setPixelColorRGB(i, 0, 0, 0)
#
#         led_strip.strip.show()
#         time.sleep(0.1)
#
#     except KeyboardInterrupt:
#         log.warn("Program interrupted")
#         color_wipe(led_strip.strip, Color(0, 0, 0), 10)
#         exit()
#
#     except Exception:
#         log.error("Any error occurs")
name = "Clock 1"


def __run():
    pass



def run_thread():
    any(thread.pause() for thread in cancel.threads)
    if not clock1_thread.isAlive():
        clock1_thread.start()
        print(name + ' thread started')
    clock1_thread.resume()
    print(name + ' is running!')
    return


clock1_thread = RaspberryThread(function=__run, name=name)
cancel.threads.append(clock1_thread)
log = logger.get_logger(name)


if __name__ == '__main__':
    __run()
