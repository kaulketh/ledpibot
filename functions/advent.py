#!/usr/bin/python
# -*- coding: utf-8 -*-

import logger
from threads.raspi import RaspberryThread
from functions import cancel


def __run():
    print('Advent is running!')


def run_thread():
    any(thread.pause() for thread in cancel.threads)
    if not advent_thread.isAlive():
        advent_thread.start()
    advent_thread.resume()
    return


log = logger.get_logger('Advent')
advent_thread = RaspberryThread(function=__run)
cancel.threads.append(advent_thread)


if __name__ == '__main__':
    __run()
