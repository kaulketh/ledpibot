#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

import os
import subprocess

from logger import LOGGER

NAME = "Service"


class OSCommand:
    logger = LOGGER
    c_prefix = "- "
    c_system = "/systemInfo"
    c_reboot = "/reboot"
    c_update = "/update"

    __menu_header = f"{NAME} functions:"

    __menu_dictionary = {
        0: c_reboot,
        1: c_system,
        2: c_update
    }

    __new_line = "\n"
    __empty = ""

    def __init__(self, command: str = None, log_msg: str = None):
        self.__logger = OSCommand.logger
        self.__log_msg = log_msg
        self.__command = command

    def execute(self):
        if self.__command is not None:
            try:
                self.__logger.info(self.__log_msg) if self.__log_msg is not None else self.__command
                os.system(self.__command)
            except Exception as e:
                self.__logger.error(f"{e}")
        else:
            raise Exception("No executable command found!")

    @classmethod
    def build_menu(cls):
        try:
            m = f"{cls.__menu_header}{cls.__new_line}"
            cls.logger.debug(f"Build service menu: {m.replace(cls.__new_line, cls.__empty)}")
            for key in cls.__menu_dictionary.keys():
                line = f"{cls.c_prefix}{cls.__menu_dictionary.get(key)}{cls.__new_line}"
                m += line
                cls.logger.debug(f"Add line to menu: {line.replace(cls.__new_line, cls.__empty)}")
            return m
        except Exception as e:
            cls.logger.error(f"{e}")

    @classmethod
    def system_info(cls):
        try:
            host = subprocess.check_output("hostname", shell=True).upper()
            ip = "IP :  " + str(subprocess.check_output("hostname -I | cut -d\' \' -f1", shell=True))
            m = subprocess.check_output(
                "free -m | awk 'NR==2{printf \"Memory :  %s / %s MB (%.0f%%)\", $3,$2,$3*100/$2 }'", shell=True)
            d = subprocess.check_output(
                "df -h | awk '$NF==\"/\"{printf \"Disk :  %d / %d GB (%s)\", $3,$2,$5}'", shell=True)
            c = subprocess.check_output(
                "top - bn1 | grep \"Cpu(s)\" | sed \"s/.*, *\\([0-9.]*\\)%* id.*/\\1/\" | "
                "awk '{print \"CPU Load :  \"100 - $1\"%\"}'", shell=True)
            return f"{host} ({OSCommand.__latest_commit()[1]}){cls.__new_line}" \
                   f"{ip}{cls.__new_line}" \
                   f"{m}{cls.__new_line}" \
                   f"{d}{cls.__new_line}" \
                   f"{c}" \
                .replace("b'", "").replace("'", "").replace("\\n", "")
        except Exception as e:
            cls.logger.error(f"{e}")

    @classmethod
    def __latest_commit(cls):
        commit = "curl -s https://api.github.com/repos/kaulketh/ledpibot/commits/master --insecure "
        latest_commit = f"{subprocess.check_output(commit, shell=True)[12:46]}" \
            .replace("b'", "").replace("'", "").replace("\\n", "")
        commit_url_text = f"[{latest_commit[0:7]}](https://github.com/kaulketh/ledpibot/commit/{latest_commit})"
        return latest_commit[0:7], commit_url_text


def reboot_device(log_msg: str = None):
    OSCommand("shutdown -r now", log_msg).execute()


def system_info():
    return OSCommand.system_info()


menu = OSCommand.build_menu()

if __name__ == '__main__':
    pass
