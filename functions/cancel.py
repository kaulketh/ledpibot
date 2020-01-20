#!/usr/bin/python
# -*- coding: utf-8 -*-

import logger

log = logger.get_logger('Cancel')
threads = []


def stop_threads():
    for thread in threads:
        thread.pause()
        if not thread.stopped() and thread.isAlive():
            log.debug('stop thread ' + thread.getName())
            print('stop thread ' + thread.getName())
            thread.stop()
    # clock.clear(led_strip.strip)
    return


def pause_threads():
    for thread in threads:
        print('found in threads and try to pause: ' + thread.name)
    any(thread.pause() for thread in threads)
    # clock.clear(led_strip.strip)
    log.debug("threads paused")
    print("threads paused")


if __name__ == '__main__':
    pass
