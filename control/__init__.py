#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

from functions import clear, dictionary_functions
from .iron_man import *
from .ledstrip import STRIP, strip_setup
from .lightfunction import LightFunction

ERROR = "An error occurred: "

stop_flag = None

clear(STRIP)


def get_stop_flag():
    global stop_flag
    return stop_flag


def set_stop_flag(flag):
    """
    Set a global stop_flag for stopping while loops.

    :type flag: bool
    """
    global stop_flag
    stop_flag = flag
    LOGGER.debug(f"Stop flag set to {stop_flag}")


def run_thread(func_name, request_id, bot):
    try:
        f = thread_function(dictionary_functions, func_name)
        LOGGER.debug(f"Init thread for function: {f}")
        t = LightFunction(
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
        for t in LightFunction.threads:
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


def off():
    peripheral_functions.get(0)()
    clear(STRIP)


peripheral_functions = {0: iron_man.close_the_eyes,
                        1: iron_man.open_the_eyes,
                        2: iron_man.blink_more_often,
                        3: off}
