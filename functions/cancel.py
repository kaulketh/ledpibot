#!/usr/bin/python
# -*- coding: utf-8 -*-

import logger

log = logger.get_logger('Cancel')
threads = []


def stop_threads():
    for thread in threads:
        thread.pause()
        print(thread.getName() + ' is stopped ' + str(thread.stopped()))
        if not thread.stopped() and thread.isAlive():
            log.debug('stopping ' + thread.getName())
            thread.stop()
            print(thread.getName() + ' has stopped ' + str(thread.stopped()))
    for thread in threads:
        print(thread.name + ' is alive ' + str(thread.isAlive()))
    return


def pause_threads():
    any(thread.pause() for thread in threads)
    log.debug("threads paused")


if __name__ == '__main__':
    pass
