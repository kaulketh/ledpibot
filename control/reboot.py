#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import datetime
import time

# noinspection PyUnresolvedReferences
from config import m_rebooted
from control import LightFunction
from control.service import reboot_device


class AutoReboot(LightFunction):
    name = "Auto Reboot"
    log = LightFunction.log

    def __init__(self, reboot_time: str, bot):
        self.__hour = reboot_time[:2]
        self.__minute = reboot_time[3:5]
        self.__hm = int(self.__hour), int(self.__minute) - 1
        self.__bot = bot
        self.__ONE_MINUTE = 60  # check interval
        super(AutoReboot, self).__init__(None, None, name=self.name,
                                         bot=self.__bot)
        AutoReboot.log.debug(f"Initialized {self.__class__.__name__} {self}")

    def __time_to_reboot(self):
        h = datetime.datetime.now().hour
        m = datetime.datetime.now().minute
        s = datetime.datetime.now().second
        # current time
        c = h, m
        # hour reached
        hr = h == self.__hm[0]
        # minute reached
        mr = m == self.__hm[1] and 0 <= s < self.__ONE_MINUTE
        return hr and mr, c

    def run(self):
        AutoReboot.log.info(
            f"{self.name} scheduled: "
            f"{self.__hour}:"
            f"{self.__minute}:"
            f"{datetime.datetime.now().second}")

        while not self.__time_to_reboot()[0]:
            # AutoReboot.log.debug(
            # f"reboot time not yet reached, "
            # f"recheck in {self.__ONE_MINUTE} seconds")
            time.sleep(self.__ONE_MINUTE)
        AutoReboot.log.debug(f"reboot takes place in 1 minute")
        time.sleep(self.__ONE_MINUTE)
        AutoReboot.log.info("try to force reboot device")

        try:
            self.__bot.external_request(msg=f"{self.name}\n{m_rebooted}",
                                        bot=self.__bot)
        except ConnectionResetError as cre:
            AutoReboot.log.error(f"{cre}")
        finally:
            reboot_device(self.name)


if __name__ == '__main__':
    pass
