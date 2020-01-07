#!/usr/bin/python
# -*- coding: utf-8 -*-
# logger/__init__py
"""
author: Thomas Kaulke, kaulketh@gmail.com
"""

from .logger import get_logger
from .logger import logging

import os, errno

try:
    os.makedirs('log')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

logging.getLogger(__name__).addHandler(logging.NullHandler())
