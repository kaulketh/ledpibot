#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

import datetime
import time

from control import CountdownThread


def is_time(t: int = 0):
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    sec = datetime.datetime.now().second
    about_time = (hour == t and minute == 0 and sec <= 5)
    return about_time


class AutoReboot(CountdownThread):
    name = "Auto reboot"

    def __init__(self, t: int):
        self.t = t
        super(AutoReboot, self).__init__(None, None, name=AutoReboot.name, n=0)

    def _process(self):
        pass

    def run(self):
        self.log.info(f"Auto reboot initialized for {self.t}:00.")
        while not is_time(self.t):
            time.sleep(2)
        from bot import external_request
        from config import rebooted
        external_request(rebooted)
        from control.service import reboot_device
        reboot_device(AutoReboot.name)


if __name__ == '__main__':
    pass
