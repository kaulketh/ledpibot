#!/usr/bin/python
# -*- coding: utf-8 -*-

import logger
from threads.raspi import RaspberryThread


def __run():
    print('Animation is running!')


def run_thread():
    from functions import cancel
    any(thread.pause() for thread in cancel.threads)
    if not animation_thread.isAlive():
        animation_thread.start()
        log.info('started')
        cancel.threads.append(animation_thread)
    else:
        animation_thread.resume()
        log.info('resumed')


animation_thread = RaspberryThread(function=__run)
log = logger.get_logger('Animation')

if __name__ == '__main__':
    __run()
