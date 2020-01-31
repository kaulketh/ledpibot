#!/usr/bin/python3
# -*- coding: utf-8 -*-
# control/__init__py
"""
author: Thomas Kaulke, kaulketh@gmail.com
"""

import logger
from functions import run_advent, run_candles, run_clock1, run_clock2, run_theater, run_rainbow, clear
from config.commands import commands
from control.led_strip import strip
from control.function_thread import LightFunctionsThread

log = logger.get_logger('Control')
clear(strip)
stop_flag = None

dictionary_threads = {
    commands[1].title(): None,
    commands[2].title(): None,
    commands[3].title(): None,
    commands[4].title(): None,
    commands[5].title(): None,
    commands[6].title(): None
}

dictionary_functions = {
        commands[1]: run_advent,
        commands[2]: run_theater,
        commands[3]: run_clock1,
        commands[4]: run_clock2,
        commands[5]: run_rainbow,
        commands[6]: run_candles
    }


def _thread_function(key):
    return dictionary_functions[key]


def get_stop_flag():
    global stop_flag
    # log.debug('stop flag requested, currently it is ' + str(stop_flag))
    return stop_flag


def run_thread(func_name):
    log.debug('Call thread for ' + func_name)
    thread = dictionary_threads.get(func_name)
    if thread is None:  # Init and start new thread
        log.debug('Thread not found in dictionary for ' + func_name)
        _init_thread(func_name)
    elif not thread.is_alive():  # Start no alive thread
        thread.start()
    elif thread.is_alive():  # resume thread if it is paused
        thread.resume()
    # _check_thread_dictionary()
    set_stop_flag(False)
    return


def stop_threads():
    set_stop_flag(True)
    for key in dictionary_threads.keys():
        thread = (dictionary_threads.get(key))
        if thread is not None and thread.is_alive():
            thread.pause()
        if thread is not None:
            log.debug('Stop thread ' + thread.getName())
            thread.stop()
            dictionary_threads[key] = None
            log.debug('Removed from dictionary: ' + thread.getName())
    log.debug("Threads stopped.")
    # _check_thread_dictionary()
    return


def set_stop_flag(flag):
    """
    Set a global stop_flag. It is required for stopping while loops.

    :type flag: bool
    """
    global stop_flag
    stop_flag = flag


# noinspection PyTypeChecker
def _init_thread(func_name):
    log.debug("Init function \'{0}\' as thread \'{1}\'".format(func_name.lower(), func_name))
    new_thread = LightFunctionsThread(function=_thread_function(func_name.lower()), name=func_name, strip=strip)
    new_thread.start()
    dictionary_threads[func_name] = new_thread
    log.debug("Added to dictionary: " + str(new_thread))
    return new_thread


def _check_thread_dictionary():
    """ for debug needed only """
    log.debug('----------------------------- Dictionary check -----------------------------')
    for key in dictionary_threads.keys():
        log.debug('key: ' + key + ', value: ' + str(dictionary_threads.get(key)))
