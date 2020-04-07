#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

from config import commands
from logger import LOGGER
from .advent import run_advent
from .candles import run_candles
from .clock1 import run_clock1
from .clock2 import run_clock2
from .clock3 import run_clock3
from .clock4 import run_clock4
from .clock5 import run_clock5
from .colors import \
    run_red, run_blue, run_green, run_orange, run_yellow, run_white, \
    run_violet, run_demo, run_stroboscope, run_demo2
from .effects import clear
from .rainbow import run_rainbow
from .theater import run_theater


def build_dictionary():
    try:
        """
        Ensure right order of functions, 
        depends on the command order 
        in ~.config.dictionary.py !!!!
        """
        dictionary = {}
        functions = [None, None,
                     # index 0 and 1 not needed, direct bot commands, as last
                     run_advent, run_candles, run_clock1, run_clock2,
                     run_rainbow, run_theater, run_red, run_blue, run_green,
                     run_yellow, run_orange, run_white, run_violet, run_demo,
                     run_stroboscope, run_clock3, run_clock4, run_clock5,
                     run_demo2, None]
        LOGGER.debug("Build dictionary of required functions")
        for i in range(len(commands)):
            f = functions[i]
            dictionary[commands[i]] = f
            LOGGER.debug(f'Added {i} : {f}')
        return dictionary
    except Exception as ex:
        LOGGER.error(f"{ex}")


dictionary_functions = build_dictionary()
