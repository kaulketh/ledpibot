#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import datetime

from control import LightFunction


class AutoReboot(LightFunction):
    name = "Auto reboot"

    def __init__(self, hour: int = 0, bot=None):
        self.__hour = hour
        self.__bot = bot
        super(AutoReboot, self).__init__(None, None, name=self.name,
                                         bot=self.__bot)

    def __reboot(self):
        from config import m_rebooted
        from control.service import reboot_device
        self.__bot.external_request(msg=m_rebooted, bot=self.__bot)
        reboot_device(self.name)

    @property
    def __hour_reached(self):
        now = datetime.datetime.now()
        return now.hour == self.__hour and now.minute == 0 and now.second <= 5

    def run(self):
        try:
            self._logger.info(f"{self.name} initialized for {self.__hour}:00.")
            while not self.__hour_reached:
                pass
            self.__reboot()
        except Exception as e:
            self._logger.error(f"{e}")


if __name__ == '__main__':
    pass
