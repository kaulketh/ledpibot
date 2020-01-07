#!/usr/bin/python
# -*- coding: utf-8 -*-

import logger
from threads.raspi import RaspberryThread


def __run():
    print('Clock is running!')


def run_thread():
    from functions import cancel
    any(thread.pause() for thread in cancel.threads)
    if not clock_thread.isAlive():
        clock_thread.start()
        log.info('started')
        cancel.threads.append(clock_thread)
    else:
        clock_thread.resume()
        log.info('resumed')


clock_thread = RaspberryThread(function=__run)
log = logger.get_logger('Clock')

if __name__ == '__main__':
    __run()
