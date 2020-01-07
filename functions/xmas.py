#!/usr/bin/python
# -*- coding: utf-8 -*-

import logger
from threads.raspi import RaspberryThread


def __run():
    print('Xmas is running!')


def run_thread():
    from functions import cancel
    any(thread.pause() for thread in cancel.threads)
    if not xmas_thread.isAlive():
        xmas_thread.start()
        log.info('started')
        cancel.threads.append(xmas_thread)
    else:
        xmas_thread.resume()
        log.info('resumed')


xmas_thread = RaspberryThread(function=__run)
log = logger.get_logger('Xmas')

if __name__ == '__main__':
    __run()
