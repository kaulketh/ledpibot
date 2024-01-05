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
from .color import OwnColors
from .colorant import run_blue, run_demo, run_demo2, run_green, run_orange, \
    run_red, run_stroboscope, run_violet, run_white, run_yellow
from .effects import run_rainbow, run_rainbow_chaser, run_rainbow_cycle, \
    run_theater

STOP = commands[0]
START = commands[1]


def assigned():
    try:
        """
        Ensure right order of functions, 
        depends on the command order 
        in config/contents.yaml
        """
        dic = {}
        funcs = [None, None,
                 # index 0 and 1 not needed, direct bot commands, also -1
                 run_advent, run_candles, run_clock1, run_clock2,
                 run_rainbow_cycle, run_theater, run_red, run_blue,
                 run_green, run_yellow, run_orange, run_white, run_violet,
                 run_demo, run_stroboscope, run_clock3, run_clock4,
                 run_clock5, run_demo2, run_clock6, run_clock7,
                 run_rainbow, run_rainbow_chaser,
                 None]

        i_clocks = 4, 5, 17, 18, 19, 21, 22
        i_colors = 8, 9, 10, 13, 11, 12, 14
        i_effects = 15, 20, 6, 23, 7, 24
        i_specials = 2, 3, 16
        indices = i_clocks, i_colors, i_effects, i_specials

        for i in range(len(commands)):
            f = funcs[i]
            dic[commands[i]] = f
            LOGGER.debug(f"function[{i:02d}] {commands[i]}: {f}")
        return dic, indices
    except Exception as ex:
        LOGGER.error(f"{ex}")


dictionary_of_functions, indices_of_functions = assigned()
