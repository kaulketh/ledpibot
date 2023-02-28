#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"
__doc__ = "Call your preferred class here."

import threading

from urllib3.exceptions import HTTPError

from bots import *
from control import peripheral_functions
from logger import LOGGER


def run():
    # telegramBot.main()
    telepotBot.main()


if __name__ == '__main__':

    try:
        threading.Thread(target=peripheral_functions.get(2)).start()
        run()

    except HTTPError as e:
        LOGGER.error("HTTP Error occurs!", e)
        exit()
