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

    menu_header = f"{NAME} functions:"

    menu_dictionary = {
        0: c_reboot,
        1: c_system,
        2: c_update
    }

    new_line = "\n"
    empty = ""

    def __init__(self, command: str = None, log_msg: str = None):
        self.log_msg = log_msg
        self.command = command

    def execute(self):
        if self.command is not None:
            try:
                self.logger.info(self.log_msg) if self.log_msg is not None else self.command
                os.system(self.command)
            except Exception as e:
                self.logger.error(f"{e}")
        else:
            raise Exception("No executable command found!")

    @classmethod
    def build_menu(cls):
        try:
            m = f"{cls.menu_header}{cls.new_line}"
            cls.logger.debug(f"Build service menu: {m.replace(cls.new_line, cls.empty)}")
            for key in cls.menu_dictionary.keys():
                line = f"{cls.c_prefix}{cls.menu_dictionary.get(key)}{cls.new_line}"
                m += line
                cls.logger.debug(f"Add line to menu: {line.replace(cls.new_line, cls.empty)}")
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
            return f"{host} ({OSCommand.latest_commit()[1]}){cls.new_line}" \
                   f"{ip}{cls.new_line}" \
                   f"{m}{cls.new_line}" \
                   f"{d}{cls.new_line}" \
                   f"{c}" \
                .replace("b'", "").replace("'", "").replace("\\n", "")
        except Exception as e:
            cls.logger.error(f"{e}")

    @classmethod
    def latest_commit(cls):
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
