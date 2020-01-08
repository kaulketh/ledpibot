#!/usr/bin/python
# -*- coding: utf-8 -*-

import logger
from threads.raspi import RaspberryThread
from functions import cancel

def __run():
    print('Animation is running!')


def run_thread():

    any(thread.pause() for thread in cancel.threads)
    if not animation_thread.isAlive():
        animation_thread.start()
    animation_thread.resume()
    return


animation_thread = RaspberryThread(function=__run)
cancel.threads.append(animation_thread)
log = logger.get_logger('Animation')

if __name__ == '__main__':
    __run()
