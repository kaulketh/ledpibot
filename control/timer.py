#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Timer
"""
import threading
import time

import logger
from config import STANDBY_MINUTES as countdown

# countdown = 0.25
name = "Timer"
log = logger.get_logger(name.title())
timer_thread = None


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


def _countdown(waiting_time_minutes):
    global timer_thread
    log.debug("Countdown started.")
    remain = waiting_time_minutes * 60
    while not timer_thread.stopped() and remain > 0:
        # timer_thread is running...
        time.sleep(1)
        remain -= 1
    if timer_thread.stopped():
        return
    else:
        timer_thread.stop()
        log.info("Automatic timer has expired.")
        _any_function()


def stop_timer():
    global timer_thread
    if timer_thread is not None and not timer_thread.stopped():
        timer_thread.stop()
        log.debug("Timer has stopped.")


def start_timer():
    global timer_thread
    timer_thread = StoppableThread(target=_countdown, args=(countdown,))
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
