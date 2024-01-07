#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"
__doc__ = "Call instance of framework class."

from urllib3.exceptions import HTTPError, ProtocolError

from app import framework
from control import peripheral_functions
from logger import LOGGER

if __name__ == '__main__':

    try:
        framework.main()
    except (ConnectionResetError, HTTPError, ProtocolError) as e:
        LOGGER.error(f"Connection error occurs: {e}")
        exit()
    finally:
        peripheral_functions.get(3)()
