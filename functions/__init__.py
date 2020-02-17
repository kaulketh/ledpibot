#!/usr/bin/python3
# -*- coding: utf-8 -*-
# functions/__init__py
"""
author: Thomas Kaulke, kaulketh@gmail.com
"""

from config import commands
from .advent import run_advent
from .candles import run_candles
from .clock1 import run_clock1
from .clock2 import run_clock2
from .clock3 import run_clock3
from .colors import \
    run_red, run_blue, run_green, run_orange, run_yellow, run_white, run_pink, run_demo, run_stroboscope
from .effects import clear
from .rainbow import run_rainbow
from .theater import run_theater

dictionary_functions = {
    commands[0]: None,  # direct bot command, no function call needed
    commands[1]: None,  # direct bot command, no function call needed
    commands[2]: run_advent,
    commands[3]: run_candles,
    commands[4]: run_clock1,
    commands[5]: run_clock2,
    commands[6]: run_rainbow,
    commands[7]: run_theater,
    commands[8]: run_red,
    commands[9]: run_blue,
    commands[10]: run_green,
    commands[11]: run_yellow,
    commands[12]: run_orange,
    commands[13]: run_white,
    commands[14]: run_pink,
    commands[15]: run_demo,
    commands[16]: run_stroboscope,
    commands[17]: run_clock3
}
""" 
Content of this dictionary depends on the possible commands, refer ~.config.dictionary.py
"""
