#!/usr/bin/python
# -*- coding: utf-8 -*-

import logger
from threads.raspi import RaspberryThread
from functions import cancel


def __run():
    print('Xmas is running!')


def run_thread():
    any(thread.pause() for thread in cancel.threads)
    if not xmas_thread.isAlive():
        xmas_thread.start()
    xmas_thread.resume()
    return


xmas_thread = RaspberryThread(function=__run)
cancel.threads.append(xmas_thread)
log = logger.get_logger('Xmas')

if __name__ == '__main__':
    __run()
