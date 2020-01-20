#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
logger.py
logging tool
"""
import os
import errno

import logging
from logging.config import fileConfig

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

try:
    os.makedirs('../log')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

this_folder = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(this_folder, 'logger.ini')
fileConfig(config_file, disable_existing_loggers=True)

# Create handlers
handler_info = logging.FileHandler(os.path.join(this_folder, '../log/info.log'))
handler_error = logging.FileHandler(os.path.join(this_folder, '../log/error.log'))
handler_info.setLevel(logging.INFO)
handler_error.setLevel(logging.ERROR)

# Create formatters and add it to handlers
format_info = \
    logging.Formatter('%(asctime)s  %(levelname)-8s '
                      '[ %(module)s.%(funcName)s '
                      'linenr: %(lineno)s ] %(message).150s', datefmt='%Y-%m-%d %H:%M:%S')
format_error = \
    logging.Formatter('%(asctime)s  %(levelname)-8s '
                      '[%(name)s] [ %(module)s.%(funcName)s  '
                      'linenr: %(lineno)s ] [ thread: %(threadName)s ] %(message)s')
handler_info.setFormatter(format_info)
handler_error.setFormatter(format_error)


def get_logger(name=None):
    if name is None:
        name = __name__
    logger = logging.getLogger(name[0:15])
    # Add handlers to the logger
    logger.addHandler(handler_info)
    logger.addHandler(handler_error)
    return logger


if __name__ == '__main__':
    pass
