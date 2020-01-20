#!/usr/bin/python
# -*- coding: utf-8 -*-

import logger
from threads.raspi import RaspberryThread
from functions import cancel

name = "Advent"


def __run():
    pass



def run_thread():
    any(thread.pause() for thread in cancel.threads)
    if not advent_thread.isAlive():
        advent_thread.start()
        print(name + ' thread started')
    advent_thread.resume()
    print(name + ' is running!')
    return


log = logger.get_logger(name)
advent_thread = RaspberryThread(function=__run, name=name)
cancel.threads.append(advent_thread)


if __name__ == '__main__':
    __run()
