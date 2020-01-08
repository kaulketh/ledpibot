#!/usr/bin/python
# -*- coding: utf-8 -*-

import logger
from threads.raspi import RaspberryThread
from functions import cancel


def __run():
    print('Clock is running!')


def run_thread():
    any(thread.pause() for thread in cancel.threads)
    if not clock_thread.isAlive():
        clock_thread.start()
    clock_thread.resume()
    return


clock_thread = RaspberryThread(function=__run)
cancel.threads.append(clock_thread)
log = logger.get_logger('Clock')

if __name__ == '__main__':
    __run()
