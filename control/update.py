#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import os

import config
from control.service import reboot_device
from logger import LOGGER

GIT = "https://github.com/kaulketh/ledpibot.git"
HOME_PI_BOT = "/home/pi/bot"
PROJECT = "ledpibot"
SECRET = config.CFG_FILES.secrets


def ignored(f):
    return f.startswith('.') or \
        f == 'hardware' or \
        f.endswith('.md') or \
        f.endswith('.MD') or \
        f == 'UNLICENSE' or \
        f == 'LICENSE'


class Update:
    name = "update"

    def __init__(self, source, target, project, branch: str = None,
                 secret: str = None):
        self.__source = source
        self.__target = target
        self.__project = project
        self.__secret = secret
        self.__log = LOGGER
        self.__branch = 'master' if branch is None else branch
        if self.__secret is not None:
            self.__save_secret = f"mv -v {self.__target}" \
                                 f"/config/{self.__secret} " \
                                 f"{self.__target}/{self.__secret}"
            self.__restore_secret = f"mv -v {self.__target}/{self.__secret} " \
                                    f"{self.__target}/config/{self.__secret}"
        else:
            self.__save_secret = ""
            self.__restore_secret = ""
        self.__remove_clone = f"rm -rf {self.__project}/"
        self.__clone = f"git clone -v {self.__source} -b {self.__branch}"
        self.__folder = os.path.dirname(os.path.abspath(__file__))
        self.__root_folder = os.path.join(self.__folder, '..')
        self.__subs = [f for f in os.listdir(self.__root_folder)]
        self.__log.debug(
            f"Initialize instance of {self.__class__.__name__} {self}")

    @property
    def run(self):
        self.__log.info("Starting update...")
        try:
            os.system(self.__save_secret)
            self.__log.info(
                f"Clone branch '{self.__branch}' from '{self.__source}'...")
            os.system(self.__clone)
            cloned_f = [f for f in os.listdir(self.__project) if
                        not ignored(f)]
            self.__log.info("Copy files and folders...")
            for f in cloned_f:
                os.system(f"cp -rv {self.__project}/{f} {self.__target}/")
            os.system(self.__restore_secret)
            self.__log.info("Remove not needed files...")
            os.system(self.__remove_clone)
        except Exception as e:
            self.__log.error(f"{e}")
            return False
        return True

    def start(self, log_str: str):
        try:
            self.__log.info(log_str)
            if self.run:
                reboot_device('Update done.')
            else:
                self.__log.warning('Update failed.')
        except Exception as e:
            self.__log.error(f"{e}")


def update_bot(log_msg: str):
    bot_update = Update(GIT, HOME_PI_BOT, PROJECT, secret=SECRET)
    bot_update.start(log_msg)


if __name__ == '__main__':
    pass
