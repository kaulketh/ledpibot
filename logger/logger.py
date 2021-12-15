#!/usr/bin/python3
# -*- coding: utf-8 -*-

import errno
import logging
import logging.handlers
import os
import sys

from clss import Singleton


class _LoggerMeta(type, Singleton):
    NAME = "Logger"
    FOLDER_PATH = "../logs"
    ADDITIONAL_DEBUG_LOG = False

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    """Runtime location"""

    LOG_FOLDER = os.path.join(THIS_FOLDER, FOLDER_PATH)
    """Defined log folder related to location"""

    # define log files, names, formats
    DEB_LOG = f"{LOG_FOLDER}/debug.log"
    INF_LOG = f"{LOG_FOLDER}/info.log"
    ERR_LOG = f"{LOG_FOLDER}/error.log"
    MAX_BYTE = 1024 ** 1024  # 1MB
    BACK_COUNT = 5

    DATE_FMT = "%Y-%m-%d %H:%M:%S"
    INF_FMT = "%(asctime)s %(levelname)s %(name)s " \
              "[%(pathname)s %(funcName)s(lnr.%(lineno)s)] %(message)s"
    ERR_FMT = "%(asctime)s %(levelname)s %(name)s " \
              "[%(pathname)s %(funcName)s(lnr.%(lineno)s)] " \
              "[thread: %(threadName)s] %(message)s"
    DEBUG_FMT = "%(asctime)s %(levelname)s %(name)s " \
                "%(pathname)s %(funcName)s(lnr.%(lineno)s) %(message)s"

    def __init__(cls, *args, **kwargs):
        super(_LoggerMeta, cls).__init__(*args, **kwargs)
        cls.__name = _LoggerMeta.NAME
        cls.__debug_log = _LoggerMeta.ADDITIONAL_DEBUG_LOG
        cls.__this_folder = _LoggerMeta.THIS_FOLDER
        cls.__log_folder = _LoggerMeta.LOG_FOLDER
        cls.__deb_log_file = _LoggerMeta.DEB_LOG
        cls.__inf_log_file = _LoggerMeta.INF_LOG
        cls.__err_log_file = _LoggerMeta.ERR_LOG

        # check if exists or create log folder
        try:
            os.makedirs(cls.__log_folder, exist_ok=True)  # Python > 3.2
        except TypeError:
            try:
                os.makedirs(cls.__log_folder)
            except OSError as exc:  # Python > 2.5
                if exc.errno == errno.EEXIST and os.path.isdir(
                        cls.__log_folder):
                    pass
                else:
                    raise

        # setup logger base configuration for console output
        logging.basicConfig(
            level=logging.DEBUG,
            stream=sys.stdout,
            datefmt=_LoggerMeta.DATE_FMT,
            format=_LoggerMeta.DEBUG_FMT)
        # create file handlers
        cls.__handler_info = logging.handlers.RotatingFileHandler(
            os.path.join(cls.__this_folder, cls.__inf_log_file),
            maxBytes=_LoggerMeta.MAX_BYTE, backupCount=_LoggerMeta.BACK_COUNT)
        cls.__handler_error = logging.handlers.RotatingFileHandler(
            os.path.join(cls.__this_folder, cls.__err_log_file),
            maxBytes=_LoggerMeta.MAX_BYTE, backupCount=_LoggerMeta.BACK_COUNT)

        # set handler log levels
        cls.__handler_info.setLevel(logging.INFO)
        cls.__handler_error.setLevel(logging.ERROR)

        # create formatters and setup handlers
        cls.__format_info = \
            logging.Formatter(_LoggerMeta.INF_FMT,
                              datefmt=_LoggerMeta.DATE_FMT)
        cls.__format_error = \
            logging.Formatter(_LoggerMeta.ERR_FMT,
                              datefmt=_LoggerMeta.DATE_FMT)

        cls.__handler_info.setFormatter(cls.__format_info)
        cls.__handler_error.setFormatter(cls.__format_error)

        # instantiate logger and add handler
        cls.__log_instance = logging.getLogger(cls.__name)

        cls.__log_instance.addHandler(cls.__handler_info)
        cls.__log_instance.addHandler(cls.__handler_error)

        # if debug.log enabled
        if cls.__debug_log:
            cls.__handler_debug = logging.handlers.RotatingFileHandler(
                os.path.join(cls.__this_folder, cls.__deb_log_file),
                maxBytes=_LoggerMeta.MAX_BYTE,
                backupCount=_LoggerMeta.BACK_COUNT)
            cls.__handler_debug.setLevel(logging.DEBUG)
            cls.__format_debug = \
                logging.Formatter(_LoggerMeta.DEBUG_FMT,
                                  datefmt=_LoggerMeta.DATE_FMT)
            cls.__handler_debug.setFormatter(cls.__format_debug)
            cls.__log_instance.addHandler(cls.__handler_debug)

    @property
    def instance(cls):
        return cls.__log_instance


class PreconfiguredLogger(metaclass=_LoggerMeta):
    pass


if __name__ == '__main__':
    pass
