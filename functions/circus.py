#!/usr/bin/python
# -*- coding: utf-8 -*-

import logger
from threads.raspi import RaspberryThread
from functions import cancel

name = "Circus"


def __run():
    pass


def run_thread():
    any(thread.pause() for thread in cancel.threads)
    if not circus_thread.isAlive():
        circus_thread.start()
        print(name + ' thread started')
    circus_thread.resume()
    print(name + ' is running!')
    return


circus_thread = RaspberryThread(function=__run, name=name)
cancel.threads.append(circus_thread)
log = logger.get_logger(name)

if __name__ == '__main__':
    __run()
