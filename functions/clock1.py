#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logger

name = "Clock 1"
log = logger.get_logger(name)


def run_clock1(strip):
    log.debug('running...' + str(strip))


if __name__ == '__main__':
    pass
