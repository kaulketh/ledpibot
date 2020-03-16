#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

import errno
import logging
import os
from logging.config import fileConfig

this_folder = os.path.dirname(os.path.abspath(__file__))

log_folder = os.path.join(this_folder, '../logs')
ini_file = 'logger.ini'
info_log_file = log_folder + '/info.log'
error_log_file = log_folder + '/error.log'

# check if exists or create log folder
try:
    os.makedirs(log_folder, exist_ok=True)  # Python>3.2
except TypeError:
    try:
        os.makedirs(log_folder)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(log_folder):
            pass
        else:
            raise

config_file = os.path.join(this_folder, ini_file)
fileConfig(config_file, disable_existing_loggers=True)

# Create handlers
handler_info = logging.FileHandler(os.path.join(this_folder, info_log_file))
handler_error = logging.FileHandler(os.path.join(this_folder, error_log_file))
handler_info.setLevel(logging.INFO)
handler_error.setLevel(logging.ERROR)

# Create formatters and add it to handlers
format_info = \
    logging.Formatter('%(asctime)s  %(levelname)-8s '
                      '[ %(module)s.%(funcName)s '
                      'linenr.%(lineno)s ] %(message).150s', datefmt='%Y-%m-%d %H:%M:%S')
format_error = \
    logging.Formatter('%(asctime)s  %(levelname)-8s '
                      '[%(name)s] [ %(module)s.%(funcName)s  '
                      'linenr.%(lineno)s ] [ thread: %(threadName)s ] %(message)s')
handler_info.setFormatter(format_info)
handler_error.setFormatter(format_error)


def get_logger(name=None):
    if name is None:
        name = __name__
    logger = logging.getLogger(name)
    # Add handlers to the logger
    logger.addHandler(handler_info)
    logger.addHandler(handler_error)
    return logger


if __name__ == '__main__':
    pass
