#!/usr/bin/python
# -*- coding: utf-8 -*-

import logger

log = logger.get_logger('Cancel')
threads = []


def stop():
    any(thread.pause() for thread in threads)
    log.info("all threads should paused")
    return


if __name__ == '__main__':
    pass
