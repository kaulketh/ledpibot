#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

from config import commands
from logger import LOGGER
from .advent import run_advent
from .candles import run_candles
from .clocks import \
    run_clock1, run_clock2, run_clock3, \
    run_clock4, run_clock5, run_clock6, run_clock7
from .colors import run_blue, run_demo, run_demo2, run_green, run_orange, \
    run_red, run_stroboscope, run_violet, run_white, run_yellow
from .effect import run_rainbow, run_theater


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
                     run_demo2, run_clock6, run_clock7, None]
        LOGGER.debug("Build functions dictionary.")
        for i in range(len(commands)):
            f = functions[i]
            dictionary[commands[i]] = f
            LOGGER.debug(f'Add {i}: {f}')
        return dictionary
    except Exception as ex:
        LOGGER.error(f"{ex}")


dictionary_functions = build_dictionary()
