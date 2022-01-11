#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"
__doc__ = "Call your preferred class here."

from concurrent.futures import ThreadPoolExecutor

from urllib3.exceptions import HTTPError

from bots import *
from control import wink_w_eyes
from logger import LOGGER


def run():
    # telegramBot.main()
    telepotBot.main()


if __name__ == '__main__':
    try:
        go_on = ThreadPoolExecutor()
        go_on.submit(run)
        go_on.submit(wink_w_eyes)
        go_on.shutdown()
    except HTTPError as e:
        LOGGER.error("HTTP Error occurs!", e)
        exit()
