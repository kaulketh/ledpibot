#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"
__doc__ = "Call instance of framework class."

import threading

from urllib3.exceptions import HTTPError, ProtocolError

from bot_framework import *
from logger import LOGGER

if __name__ == '__main__':

    try:
        threading.Thread(target=peripheral_functions.get(2)).start()
        telepot_bot.main()
    except (ConnectionResetError, ProtocolError, HTTPError) as e:
        LOGGER.error(f"Connection error occurs: {e}")
        exit()
    finally:
        peripheral_functions.get(3)()
