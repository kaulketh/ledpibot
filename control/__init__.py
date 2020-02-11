#!/usr/bin/python3
# -*- coding: utf-8 -*-
# control/__init__py
"""
Control light functions and effects
"""

import logger
from control.function_thread import LightFunctionsThread
from control.led_strip import strip
from functions import clear, dictionary_functions

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

log = logger.get_logger('Control')
stop_flag = None
dictionary_threads = {'None': None}

clear(strip)


def _thread_function(dictionary, key):
    try:
        return dictionary[key]
    except Exception as e:
        log.error('An error occurs: ' + str(e))


def get_stop_flag():
    global stop_flag
    return stop_flag


def run_thread(func_name):
    stop_threads()
    try:
        log.info('Start thread: ' + func_name)
        thread = dictionary_threads.get(func_name)
        if thread is None:
            log.debug('Not found in dictionary: ' + func_name)
            _init_thread(func_name)
        elif not thread.is_alive():
            thread.start()
        elif thread.is_alive():
            thread.resume()
        set_stop_flag(False)
        return
    except Exception as e:
        log.error('An error occurs: ' + str(e))


def stop_threads():
    set_stop_flag(True)
    try:
        for key in dictionary_threads.keys():
            thread = (dictionary_threads.get(key))
            if thread is not None and thread.is_alive():
                thread.pause()
            if thread is not None:
                log.info('Stop thread: ' + thread.getName())
                thread.stop()
                dictionary_threads[key] = None
                log.debug('Removed from dictionary: ' + thread.getName())
        log.debug("Threads stopped.")
        return
    except Exception as e:
        log.error('An error occurs: ' + str(e))


def set_stop_flag(flag):
    """
    Set a global stop_flag. It is necessary for stopping while loops.

    :type flag: bool
    """
    global stop_flag
    stop_flag = flag


# noinspection PyTypeChecker
def _init_thread(func_name):
    log.debug("Init function \'{0}\' as thread \'{0}\'".format(func_name))
    new_thread = LightFunctionsThread(
        function=_thread_function(dictionary_functions, func_name),
        name=func_name,
        strip=strip)
    new_thread.start()
    dictionary_threads[func_name] = new_thread
    log.debug("Added to dictionary: " + str(new_thread))
    return new_thread
