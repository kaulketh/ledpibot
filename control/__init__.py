#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

from functions import dictionary_functions
from functions.effects import clear
from .iron import *
from .light import LightFunction
from .wreath import WREATH, wreath_setup

ERROR = "Any error occurred: "

stop_flag = None

clear(WREATH)


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
        f = dictionary_functions.get(func_name)
        LOGGER.debug(f"Init thread for function: {f}")
        t = LightFunction(
            function=f,
            wreath=WREATH,
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


def off():
    peripheral_functions.get(0)()
    clear(WREATH)


peripheral_functions = {0: iron_man.close_the_eyes,
                        1: iron_man.open_the_eyes,
                        2: iron_man.blink_more_often,
                        3: off}
"""dictionary of some functions:\n
0 - to close Iron Man's eyes,\n 
1 - to open Iron Man's eyes,\n 
2 - to let Iron Man blink with eyes,\n 
3 - to turn off all LEDs"""
