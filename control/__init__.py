#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

import logger
from functions import dictionary_functions, clear
from .countdown import CountdownThread
from .led_strip import strip, set_brightness_depending_on_daytime

LOG = logger.get_logger(__name__)
ERROR = "An error occurs: "

stop_flag = None

clear(strip)


def get_stop_flag():
    global stop_flag
    return stop_flag


def set_stop_flag(flag):
    """
    Set a global stop_flag. It is necessary for stopping while loops.

    :type flag: bool
    """
    global stop_flag
    stop_flag = flag


def run_thread(func_name):
    try:
        if stop_threads():
            f = _thread_function(dictionary_functions, func_name)
            LOG.debug(f"Init thread for function: {f}")
            t = CountdownThread(
                function=f,
                stripe=strip,
                name=func_name)
            t.start()
            set_stop_flag(False)
            return t
    except Exception as e:
        LOG.error(f"{ERROR}{e}")


def stop_threads():
    set_stop_flag(True)
    try:
        for t in CountdownThread.threads:
            if t is not None and t.is_running:
                t.stop()
        return True
    except Exception as e:
        LOG.error(f"{ERROR}{e}")
    return False


def _thread_function(dictionary, key):
    try:
        return dictionary[key]
    except Exception as e:
        LOG.error(f"{ERROR}{e}")
