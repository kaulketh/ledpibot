#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

from .logger import get_logger
from .logger import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
