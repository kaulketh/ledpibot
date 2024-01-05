#!/usr/bin/python3
# -*- coding: utf-8 -*-

import errno
import logging
import logging.handlers
import os
import sys

import yaml

# Load settings
FILE = "logger.yaml"
HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, FILE), 'r', encoding='utf-8') as file:
    logger_settings = yaml.safe_load(file)
# Load values into constants dynamically
for item in logger_settings.items():
    _name = item[0]
    _value = item[1]
    globals()[_name] = _value


class _Singleton(type):
    """ A metaclass that creates a Singleton base class when called. """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args,
                                                                  **kwargs)
        return cls._instances[cls]


class Singleton(_Singleton('SingletonMeta', (object,), {})):
    pass


# noinspection PyUnresolvedReferences
class _LoggerMeta(type, Singleton):
    NAME = LOGGER_NAME
    FOLDER_PATH = f"../{DIRECTORY}"
    ADDITIONAL_DEBUG_LOG = DEBUG_LOG
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    """Runtime location"""
    LOG_FOLDER = os.path.join(THIS_FOLDER, FOLDER_PATH)
    """Defined log folder related to location"""
    # log files, names, formats
    DEB_LOG = f"{LOG_FOLDER}/{DEBUG_FILE}"
    INF_LOG = f"{LOG_FOLDER}/{INFO_FILE}"
    ERR_LOG = f"{LOG_FOLDER}/{ERROR_FILE}"
    HIS_LOG = f"{LOG_FOLDER}/{HISTORY_FILE}"
    MAX_BYTE = FILE_SIZE
    BACK_COUNT = FILE_COUNT
    # log formats
    DAT_FMT = "%Y-%m-%d %H:%M:%S"
    __P1 = "%(asctime)s %(name)s %(levelname)s"
    __P2 = "%(pathname)s %(funcName)s(lnr.%(lineno)s)"
    __P3 = "%(message)s"
    INF_FMT = f"{__P1} [{__P2}] {__P3}"
    ERR_FMT = f"{__P1} [{__P2}] [thread: %(threadName)s] {__P3}"
    DEB_FMT = f"{__P1} {__P2} {__P3}"
    HIS_FMT = f"{__P1} {__P3}"
    HISTORY = 39  # before error level

    # noinspection PyProtectedMember
    def __init__(cls, *args, **kwargs):
        super(_LoggerMeta, cls).__init__(*args, **kwargs)
        cls.__name = _LoggerMeta.NAME
        cls.__debug_log = _LoggerMeta.ADDITIONAL_DEBUG_LOG
        cls.__this_folder = _LoggerMeta.THIS_FOLDER
        cls.__log_folder = _LoggerMeta.LOG_FOLDER
        cls.__deb_log_file = _LoggerMeta.DEB_LOG
        cls.__inf_log_file = _LoggerMeta.INF_LOG
        cls.__err_log_file = _LoggerMeta.ERR_LOG
        cls.__his_log_file = _LoggerMeta.HIS_LOG

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
            datefmt=_LoggerMeta.DAT_FMT,
            format=_LoggerMeta.DEB_FMT)
        # create file handlers
        cls.__handler_info = logging.handlers.RotatingFileHandler(
            os.path.join(cls.__this_folder, cls.__inf_log_file),
            maxBytes=_LoggerMeta.MAX_BYTE, backupCount=_LoggerMeta.BACK_COUNT)
        cls.__handler_error = logging.handlers.RotatingFileHandler(
            os.path.join(cls.__this_folder, cls.__err_log_file),
            maxBytes=_LoggerMeta.MAX_BYTE, backupCount=_LoggerMeta.BACK_COUNT)
        cls.__handler_history = logging.handlers.RotatingFileHandler(
            os.path.join(cls.__this_folder, cls.__his_log_file),
            maxBytes=_LoggerMeta.MAX_BYTE, backupCount=_LoggerMeta.BACK_COUNT)

        # set handler log levels
        cls.__handler_info.setLevel(logging.INFO)
        cls.__handler_error.setLevel(logging.ERROR)
        # add custom log level
        logging.addLevelName(_LoggerMeta.HISTORY, 'HISTORY')
        cls.__handler_history.setLevel(_LoggerMeta.HISTORY)

        # create formatters and setup handlers
        cls.__format_info = \
            logging.Formatter(_LoggerMeta.INF_FMT,
                              datefmt=_LoggerMeta.DAT_FMT)
        cls.__format_error = \
            logging.Formatter(_LoggerMeta.ERR_FMT,
                              datefmt=_LoggerMeta.DAT_FMT)
        cls.__format_history = \
            logging.Formatter(_LoggerMeta.HIS_FMT,
                              datefmt=_LoggerMeta.DAT_FMT)

        cls.__handler_info.setFormatter(cls.__format_info)
        cls.__handler_error.setFormatter(cls.__format_error)
        cls.__handler_history.setFormatter(cls.__format_history)

        # instantiate logger and add handler
        cls.__instance = logging.getLogger(cls.__name)

        cls.__instance.addHandler(cls.__handler_info)
        cls.__instance.addHandler(cls.__handler_error)
        cls.__instance.addHandler(cls.__handler_history)

        # if debug.log enabled
        if cls.__debug_log:
            cls.__handler_debug = logging.handlers.RotatingFileHandler(
                os.path.join(cls.__this_folder, cls.__deb_log_file),
                maxBytes=_LoggerMeta.MAX_BYTE,
                backupCount=_LoggerMeta.BACK_COUNT)
            cls.__handler_debug.setLevel(logging.DEBUG)
            cls.__format_debug = \
                logging.Formatter(_LoggerMeta.DEB_FMT,
                                  datefmt=_LoggerMeta.DAT_FMT)
            cls.__handler_debug.setFormatter(cls.__format_debug)
            cls.__instance.addHandler(cls.__handler_debug)

        # set custom log level
        cls.__instance.history = \
            lambda msg, *ars: cls.__instance._log(cls.HISTORY, msg, ars)

        cls.__instance.debug(
            f"Initialize instance of {cls.__name__} {cls}")

    @property
    def instance(cls):
        return cls.__instance

    @property
    def log_folder(cls):
        return cls.__log_folder


class PreconfiguredLogger(metaclass=_LoggerMeta):
    pass


if __name__ == '__main__':
    pass
