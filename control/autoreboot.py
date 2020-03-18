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
        self.hour = hour
        super(AutoReboot, self).__init__(None, None, name=self.name, n=0)

    def start(self) -> None:
        self.run()
        return

    def __process(self):
        pass

    def run(self):
        try:
            self.logger.info(f"{self.name} initialized for {self.hour}:00.")
            while not self.__time_reached:
                time.sleep(2)
            from bot import external_request
            from config import rebooted
            external_request(rebooted)
            from control.service import reboot_device
            reboot_device(self.name)
        except Exception as e:
            self.logger.error(f"{e}")

    @property
    def __time_reached(self):
        now = datetime.datetime.now()
        return now.hour == self.hour and now.minute == 0 and now.second <= 5


if __name__ == '__main__':
    pass
