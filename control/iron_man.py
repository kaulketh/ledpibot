#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import os
import time

from logger import LOGGER
from config import IP_MASK_IRONMAN, PORT_MASK_IRONMAN

WEB_SERVER_IP = IP_MASK_IRONMAN
WEB_SERVER_PORT = PORT_MASK_IRONMAN
# noinspection HttpUrlsUsage
CURL = f"curl --silent --output nul " \
       f"http://{WEB_SERVER_IP}:{WEB_SERVER_PORT}" \
       f"/?mode="
OFF = "0 &"
ON = "1 &"


def close_the_eyes():
    LOGGER.info("Iron Man closes the eyes.")
    os.system(f"{CURL}{OFF}")


def open_the_eyes():
    LOGGER.info("Iron Man opens the eyes.")
    os.system(f"{CURL}{ON}")


def wink_w_eyes(wink=5, opened=.5, closed=.25):
    LOGGER.info(f"Iron Man {wink} times winks with eyes.")
    while wink > 0:
        os.system(f"{CURL}1 &")
        time.sleep(opened)
        os.system(f"{CURL}0 &")
        time.sleep(closed)
        wink -= 1


if __name__ == '__main__':
    pass
