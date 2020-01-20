#!/usr/bin/python
# -*- coding: utf-8 -*-

import logger
from threads.raspi import RaspberryThread
from functions import cancel

name = "Theater"


def __run():
    pass


def run_thread():
    any(thread.pause() for thread in cancel.threads)
    if not theater_thread.isAlive():
        theater_thread.start()
        print(name + ' thread started')
    theater_thread.resume()
    print(name + ' is running!')
    return


theater_thread = RaspberryThread(function=__run, name=name)
cancel.threads.append(theater_thread)
log = logger.get_logger(name)

if __name__ == '__main__':
    __run()
