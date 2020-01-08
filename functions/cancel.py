#!/usr/bin/python
# -*- coding: utf-8 -*-

import logger
from functions import clock, led_strip

log = logger.get_logger('Cancel')
threads = []


def stop_threads():
    for thread in threads:
        thread.pause()
        if not thread.stopped() and thread.isAlive():
            log.debug('stopping ' + thread.getName())
            thread.stop()
    clock.clear(led_strip.strip)
    return


def pause_threads():
    any(thread.pause() for thread in threads)
    clock.clear(led_strip.strip)
    log.debug("threads paused")


if __name__ == '__main__':
    pass
