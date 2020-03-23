#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

import os

from control.service import reboot_device
from logger import LOGGER


class Update:
    logger = LOGGER
    name = "update"

    def __init__(self, branch: str = None):
        self.__branch = 'master' if branch is None else branch
        self.__save_secret = 'mv -v /home/pi/bot/config/secret.py /home/pi/bot/secret.py'
        self.__restore_secret = 'mv -v /home/pi/bot/secret.py /home/pi/bot/config/secret.py'
        self.__remove_clone = 'rm -rf ledpibot/'
        self.__clone = 'git clone -v https://github.com/kaulketh/ledpibot.git -b ' + self.__branch
        self.__folder = os.path.dirname(os.path.abspath(__file__))
        self.__root_folder = os.path.join(self.__folder, '..')
        self.__subs = [f for f in os.listdir(self.__root_folder)]

    @staticmethod
    def __ignored(f_name: str):
        return f_name.startswith('.') or f_name == 'hardware'

    @property
    def run(self):
        self.logger.info("Starting update...")
        try:
            os.system(self.__save_secret)
            self.logger.info(f"Clone branch \'{self.__branch}\' from Github repository...")
            os.system(self.__clone)
            cloned_f = [f for f in os.listdir('ledpibot') if not self.__ignored(f)]
            self.logger.info("Copy files and folders...")
            for f in cloned_f:
                os.system('cp -rv ledpibot/' + f + ' /home/pi/bot/')
            os.system(self.__restore_secret)
            self.logger.info("Remove not needed files...")
            os.system(self.__remove_clone)
        except Exception as e:
            self.logger.error(f"Update failure: {e}")
            return False
        return True


def update_bot(log_msg: str):
    try:
        Update.logger.info(log_msg)
        if Update().run:
            reboot_device('Update done.')
        else:
            Update.logger.warning('Update failed.')
    except Exception as e:
        Update.logger.error(f"{e}")


if __name__ == '__main__':
    pass
