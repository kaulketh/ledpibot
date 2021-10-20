#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import datetime
import time

from config import m_rebooted
from control import LightFunction


class AutoReboot(LightFunction):
    name = "Auto Reboot"

    def __init__(self, hour: int = 0, bot=None, check_interval=60):
        self.__hour = hour
        self.__bot = bot
        self.__check_interval = check_interval
        super(AutoReboot, self).__init__(None, None, name=self.name,
                                         bot=self.__bot)

        self.start()

    @staticmethod
    def __time_has_been_reached(hour_to_be_reached):
        return datetime.datetime.now().hour == hour_to_be_reached

    def __reboot(self):
        from control.service import reboot_device
        self.__bot.external_request(msg=f"{self.name}:\n"
                                        f"{m_rebooted}",
                                    bot=self.__bot)
        reboot_device(self.name)

    def run(self):
        try:
            self._logger.info(
                f"Initialized {self.name} at {self.__hour}:00 h.")
            while not self.__time_has_been_reached(self.__hour):
                time.sleep(self.__check_interval)
            self.__reboot()
        except Exception as e:
            self._logger.error(f"{e}")


if __name__ == '__main__':
    pass
