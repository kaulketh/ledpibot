#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

import datetime
import time

from control import CountdownThread


class AutoReboot(CountdownThread):
    name = "Auto reboot"

    def __init__(self, hour: int = 0):
        self._hour = hour
        super(AutoReboot, self).__init__(None, None, name=self.name, n=0)

    def _process(self):
        pass

    def run(self):
        self.log.info(f"{self.name} initialized for {self._hour}:00.")
        while not self._time_reached:
            time.sleep(2)
        from bot import external_request
        from config import rebooted
        external_request(rebooted)
        from control.service import reboot_device
        reboot_device(self.name)

    @property
    def _time_reached(self):
        now = datetime.datetime.now()
        print(now)
        return now.hour == self._hour and now.minute == 0 and now.second <= 5


if __name__ == '__main__':
    pass
