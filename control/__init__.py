#!/usr/bin/python3
# -*- coding: utf-8 -*-
# control/__init__py
"""
Control light functions and effects
"""
import time
from multiprocessing import Queue
from threading import Thread

import logger
from config import STANDBY_MINUTES as COUNTDOWN, LED_BRIGHTNESS
from functions import clear, dictionary_functions
from .led_strip import strip, set_brightness_depending_on_daytime

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

NAME = "Thread Control"
LOG = logger.get_logger(NAME)
EXPIRED = "Runtime expired"
STOPPED = "Stop requested, stopped"
THREADS = []
stop_flag = None

clear(strip)


class CountdownThread(Thread):
    def __init__(self, function, stripe, name=None, n=COUNTDOWN):
        super(CountdownThread, self).__init__()
        self.n = n * 60
        self.do_run = True
        self._function = function
        self._strip = stripe
        self._queue = Queue()
        if name is None:
            self._name = function
        else:
            self._name = name

    def _thread(self):
        LOG.debug("Start function thread for {1} seconds: {0}".format(str(self._name), str(self.n)))
        func_thread = Thread(target=self._function, name=self._name, args=(self._strip,))
        func_thread.start()
        return func_thread

    def run(self):
        t = self._thread()
        THREADS.append(self)
        while self.__getattribute__('do_run') and self.n > 0 and self._queue.empty():
            self.n -= 1
            time.sleep(1)
        if self.n <= 0:
            LOG.inf("{0}: {1}".format(EXPIRED, str(self._name)))
            self._queue.put(EXPIRED)
        clear(self._strip)
        t.join()
        THREADS.remove(self)

    def stop(self):
        self._queue.put(STOPPED)
        self.do_run = False
        LOG.info("{0}: {1}".format(STOPPED, str(self._name)))

    @staticmethod
    def all_threads():
        for t in THREADS:
            yield t


def get_stop_flag():
    global stop_flag
    return stop_flag


def set_stop_flag(flag):
    """
    Set a global stop_flag. It is necessary for stopping while loops.

    :type flag: bool
    """
    global stop_flag
    stop_flag = flag


def run_thread(func_name):
    if stop_threads():
        LOG.debug("Init function \'{0}\' as thread \'{0}\'".format(func_name))
        t = CountdownThread(function=_thread_function(dictionary_functions, func_name), stripe=strip, name=func_name)
        t.start()
        set_stop_flag(False)
        return t


def stop_threads():
    set_stop_flag(True)
    clear(strip)
    try:
        for t in CountdownThread.all_threads():
            if t is not None and t.is_alive():
                t.stop()
        strip.setBrightness(LED_BRIGHTNESS)
        return True
    except Exception as e:
        LOG.error('An error occurs: ' + str(e))
    return False


def _thread_function(dictionary, key):
    try:
        return dictionary[key]
    except Exception as e:
        LOG.error('An error occurs: ' + str(e))
