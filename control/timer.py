#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Timer
"""
import threading
import time

import logger

from config import STANDBY_MINUTES as COUNTDOWN

name = "Timer"
log = logger.get_logger(name.title())
timer_thread = None


class _CountdownThread(threading.Thread):
    """Starts a specified function after specified minutes."""
    def __init__(self, minutes, function):
        super(_CountdownThread, self).__init__()
        self._seconds = minutes * 60
        self._function = function
        self.do_run = True

    def run(self):
        log.debug("Countdown started for {0} seconds.".format(str(self._seconds)))
        while self.__getattribute__('do_run') and self._seconds > 0:
            time.sleep(1)
            self._seconds -= 1
        if not self.do_run:
            log.info("Countdown stopped.")
        else:
            log.info("Countdown expired.")
            self._function()

    @property
    def stopped(self):
        return not self.do_run


def stop_timer():
    global timer_thread
    if timer_thread is not None and not timer_thread.stopped:
        timer_thread.do_run = False
        log.debug("Timer has stopped.")


def start_timer():
    global timer_thread
    timer_thread = _CountdownThread(COUNTDOWN, _any_function)
    timer_thread.start()
    log.debug("Start timer thread.")
    return


def _any_function():
    from bot import external_request
    from config import standby
    from control import stop_threads
    stop_threads()
    external_request(standby)


if __name__ == '__main__':
    pass
