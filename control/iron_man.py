#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import os
import time

from logger import LOGGER

WEB_SERVER_IP = "192.168.0.99"
WEB_SERVER_PORT = 80
# noinspection HttpUrlsUsage
CURL = f"curl --silent --output nul " \
       f"http://{WEB_SERVER_IP}:{WEB_SERVER_PORT}" \
       f"/?mode="
OFF = "0 &"
ON = "1 &"


def close_the_eyes():
    LOGGER.info("Try to close Iron Man's eyes...")
    os.system(f"{CURL}{OFF}")


def open_the_eyes():
    LOGGER.info("Try to open Iron Man's eyes...")
    os.system(f"{CURL}{ON}")


def wink_w_eyes(wink=5, opened=0.3, closed=0.15):
    LOGGER.info("Try to wink with Iron Man's eyes...")
    while wink > 0:
        os.system(f"{CURL}1 &")
        time.sleep(opened)
        os.system(f"{CURL}0 &")
        time.sleep(closed)
        wink -= 1


if __name__ == '__main__':
    pass
