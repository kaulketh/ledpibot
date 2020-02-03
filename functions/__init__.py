#!/usr/bin/python3
# -*- coding: utf-8 -*-
# functions/__init__py
"""
author: Thomas Kaulke, kaulketh@gmail.com
"""

from config import commands
from functions.advent import run_advent
from functions.candles import run_candles
from functions.clock1 import run_clock1
from functions.clock2 import run_clock2
from functions.colors import run_red, run_blue, run_green, run_orange, run_yellow, run_white, run_pink
from functions.effects import clear
from functions.rainbow import run_rainbow
from functions.theater import run_theater

dictionary_functions = {
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
    commands[14]: run_pink
}
