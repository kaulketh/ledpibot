#!/usr/bin/python
# -*- coding: utf-8 -*-

import logger
from threads.raspi import RaspberryThread
from functions import cancel

name = "Candles"


def __run():
    pass



def run_thread():
    any(thread.pause() for thread in cancel.threads)
    if not candles_thread.isAlive():
        candles_thread.start()
        print(name + ' thread started')
    candles_thread.resume()
    print(name + ' is running!')
    return


log = logger.get_logger(name)
candles_thread = RaspberryThread(function=__run, name=name)
cancel.threads.append(candles_thread)


if __name__ == '__main__':
    __run()
