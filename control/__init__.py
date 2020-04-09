#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

from functions import dictionary_functions, clear
from logger import LOGGER
from .countdown import CountdownThread
from .ledstrip import STRIP, set_brightness_depending_on_daytime

ERROR = "An error occurs: "

stop_flag = None

clear(STRIP)


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
    LOGGER.debug(f"Stop flag set: {stop_flag}")


def run_thread(func_name, request_id, bot):
    try:
        f = thread_function(dictionary_functions, func_name)
        LOGGER.debug(f"Init thread for function: {f}")
        t = CountdownThread(
            function=f,
            stripe=STRIP,
            name=func_name,
            request_id=request_id,
            bot=bot)
        t.start()
        set_stop_flag(False)
        return t
    except Exception as e:
        LOGGER.error(f"{ERROR}{e}")


def stop_threads():
    try:
        for t in CountdownThread.threads:
            if t is not None and t.is_running:
                t.stop()
        set_stop_flag(True)
    except Exception as e:
        LOGGER.error(f"{ERROR}{e}")
        set_stop_flag(False)

    return stop_flag


def thread_function(dictionary, key):
    try:
        return dictionary[key]
    except Exception as e:
        LOGGER.error(f"{ERROR}{e}")
