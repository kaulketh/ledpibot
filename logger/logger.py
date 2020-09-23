#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

import errno
import logging
import os
from logging.config import fileConfig

# runtime location
this_folder = os.path.dirname(os.path.abspath(__file__))
# define log folder related to location
log_folder = os.path.join(this_folder, '../logs')

# define ini and log files
ini_file = 'debug.ini'
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

# setup configuration
config_file = os.path.join(this_folder, ini_file)
fileConfig(config_file, disable_existing_loggers=True)

# create handlers
handler_info = logging.FileHandler(os.path.join(this_folder, info_log_file))
handler_error = logging.FileHandler(os.path.join(this_folder, error_log_file))
# set levels
handler_info.setLevel(logging.INFO)
handler_error.setLevel(logging.ERROR)

# create formatters and add to handlers
format_info = \
    logging.Formatter('%(asctime)s  %(levelname)s '
                      '[ %(module)s.%(funcName)s  linenr.%(lineno)s ] '
                      '%(message).180s', datefmt='%Y-%m-%d %H:%M:%S')
format_error = \
    logging.Formatter(
        '%(asctime)s  %(levelname)s '
        '[ %(module)s.%(funcName)s  linenr.%(lineno)s ] '
        '[ thread: %(threadName)s ] %(message)s')
handler_info.setFormatter(format_info)
handler_error.setFormatter(format_error)


def get_logger(name: str = __name__):
    logger = logging.getLogger(name)
    # add handler
    logger.addHandler(handler_info)
    logger.addHandler(handler_error)
    return logger


if __name__ == '__main__':
    pass
