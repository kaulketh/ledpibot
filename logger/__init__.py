#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
logger/__init__py
"""

from .logger import get_logger
from .logger import logging

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

logging.getLogger(__name__).addHandler(logging.NullHandler())
