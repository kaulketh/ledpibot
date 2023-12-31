#!/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# logfiles
# created 31.12.2023
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------

APP_NAME = "LedPi"
DEBUG_LOG = True
DIRECTORY = "logs"
EXTENSION = "log"

DEBUG_FILE = f"debug.{EXTENSION}"
ERROR_FILE = f"error.{EXTENSION}"
HISTORY_FILE = f"history.{EXTENSION}"
INFO_FILE = f"info.{EXTENSION}"

FILE_COUNT = 5
FILE_SIZE = 3_145_728  # 3MB

if __name__ == '__main__':
    pass
