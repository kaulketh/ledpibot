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

    def __init__(self, hour: int = 0, bot=None):
        self.__hour = hour
        self.__bot = bot
        super(AutoReboot, self).__init__(None, None, name=self.name, n=0, bot=self.__bot)

    def __process(self):
        pass

    def __reboot(self):
        from bot import LedPiBot
        from config import rebooted
        from control.service import reboot_device
        LedPiBot.external_request(msg=rebooted, bot=self.__bot)
        reboot_device(self.name)

    @property
    def __time_reached(self):
        now = datetime.datetime.now()
        return now.hour == self.__hour and now.minute == 0 and now.second <= 5

    def run(self):
        try:
            self._logger.info(f"{self.name} initialized for {self.__hour}:00.")
            while not self.__time_reached:
                time.sleep(2)
            self.__reboot()
        except Exception as e:
            self._logger.error(f"{e}")


if __name__ == '__main__':
    pass
