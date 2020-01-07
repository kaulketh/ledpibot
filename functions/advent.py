#!/usr/bin/python
# -*- coding: utf-8 -*-

import logger
from threads.raspi import RaspberryThread


def __run():
    print('Advent is running!')


def run_thread():
    from functions import cancel
    any(thread.pause() for thread in cancel.threads)
    if not advent_thread.isAlive():
        advent_thread.start()
        log.info('started')
        cancel.threads.append(advent_thread)
    else:
        advent_thread.resume()
        log.info('resumed')


advent_thread = RaspberryThread(function=__run)
log = logger.get_logger('Advent')

if __name__ == '__main__':
    __run()
