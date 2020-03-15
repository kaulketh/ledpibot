#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

import datetime
import time

import logger
from control import CountdownThread

NAME = "Auto reboot"
LOG = logger.get_logger(NAME)


def is_time(t: int = 0):
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    sec = datetime.datetime.now().second
    about_time = (hour == t and minute == 0 and sec <= 5)
    return about_time


class AutoReboot(CountdownThread):
    def __init__(self, t):
        self.t = t
        super(AutoReboot, self).__init__(None, None, name=NAME, n=0)

    def _process(self):
        pass

    def run(self):
        LOG.info("Auto reboot initialized for " + str(self.t) + " o'clock.")
        while not is_time(self.t):
            time.sleep(2)
        from bot import external_request
        from config import rebooted
        external_request(rebooted)
        from control.service import reboot_device
        reboot_device(NAME)


if __name__ == '__main__':
    pass
