#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

from functions import dictionary_of_functions
from functions.effects import clear
from logger import LOGGER
from .light import LightFunction
from .wreath import WREATH, wreath_setup

ERROR = "Any error occurred: "
flag = None

clear(WREATH)


def stopped():
    global flag
    return flag


def set_stop_flag(_flag):
    """
    Set a global stop flag for stopping while loops.

    :type _flag: bool
    """
    global flag
    flag = _flag
    LOGGER.debug(f"Stop flag: {flag}")


def run_thread(func_name, request_id, bot):
    try:
        f = dictionary_of_functions.get(func_name)
        LOGGER.debug(f"Init thread for function: {f}")
        t = LightFunction(
            function=f,
            wreath=WREATH,
            name=func_name,
            request_id=request_id,
            bot=bot)
        LOGGER.history(func_name)
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

    return flag


def off():
    clear(WREATH)


def _pass():
    pass


peripheral_functions = {0: _pass,
                        1: _pass,
                        2: _pass,
                        3: off}
"""dictionary of peripheral functions:\n
0 - pass,\n 
1 - pass,\n 
2 - pass,\n 
3 - to turn off all LEDs"""
